import os
import logging
from pathlib import Path
from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChurnLogitModel")

class EconometricChurnModel:
    def __init__(self, gold_dir: str = "data/gold/"):
        self.gold_dir = Path(gold_dir)
        self.results_dir = Path("docs/MODELS_RESULTS/")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Iniciar Spark (necesario para leer Delta localmente)
        self.spark = SparkSession.builder \
            .appName("OmniVoC-ChurnLogit") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .master("local[*]") \
            .getOrCreate()

    def load_data(self) -> pd.DataFrame:
        logger.info("Cargando Fact_Reviews desde Gold Layer...")
        fact_path = str(self.gold_dir / "Fact_Reviews")
        if not os.path.exists(fact_path):
            raise FileNotFoundError(f"No se encontró la tabla en {fact_path}")
            
        df_spark = self.spark.read.format("delta").load(fact_path)
        # Convertir a Pandas. Considerar muestreo si el volumen es excesivo para memoria (ahora son ~60k, entra bien)
        df = df_spark.toPandas()
        logger.info(f"Datos cargados: {df.shape[0]} filas.")
        return df

    def preprocess(self, df: pd.DataFrame):
        logger.info("Preprocesando variables para el modelo Logit...")
        
        # Filtramos columnas necesarias
        features = ['content_length', 'hour_of_day', 'appVersion', 'has_bank_reply', 'is_churn_risk']
        df_model = df[features].copy()
        
        # Eliminar filas con nulos en estas variables estrictas
        df_model = df_model.dropna(subset=['is_churn_risk', 'has_bank_reply'])
        
        # Asegurar tipos
        df_model['content_length'] = df_model['content_length'].fillna(0).astype(int)
        df_model['hour_of_day'] = df_model['hour_of_day'].fillna(12).astype(int)
        df_model['has_bank_reply'] = df_model['has_bank_reply'].astype(int)
        df_model['is_churn_risk'] = df_model['is_churn_risk'].astype(int)
        df_model['appVersion'] = df_model['appVersion'].fillna('UNKNOWN').astype(str)
        
        # Agrupar versiones minoritarias para evitar Perfect Multicollinearity (Matriz Singular)
        top_versions = df_model['appVersion'].value_counts().nlargest(5).index.tolist()
        df_model['appVersion'] = df_model['appVersion'].apply(lambda x: x if x in top_versions else 'OTHER_VERSION')
        
        # One-Hot Encoding
        df_model = pd.get_dummies(df_model, columns=['appVersion'], drop_first=True, dtype=int)
        
        # Opcional: Estandarizar variables continuas fuertes para ayudar a la convergencia (evitar overflow exp)
        df_model['content_length'] = (df_model['content_length'] - df_model['content_length'].mean()) / df_model['content_length'].std()
        
        X = df_model.drop(columns=['is_churn_risk'])
        y = df_model['is_churn_risk']
        
        # Añadir constante para statsmodels (intercepto)
        X = sm.add_constant(X)
        
        return X, y

    def train_and_evaluate(self, X, y):
        logger.info("Entrenando modelo Logit Econométrico (statsmodels)...")
        
        # Split Train/Test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Entrenar Statsmodels
        try:
            logit_model = sm.Logit(y_train, X_train)
            result = logit_model.fit(disp=False) # disp=False oculta prints iterativos
            summary_str = result.summary().as_text()
            logger.info("Modelo ajustado correctamente.")
        except Exception as e:
            logger.error(f"Error al ajustar el modelo (¿problemas de varianza nula/multicolinealidad?): {e}")
            raise e
            
        # Predicción sobre Test
        y_pred_prob = result.predict(X_test)
        y_pred = (y_pred_prob >= 0.5).astype(int)
        
        # Evaluar Scikit-Learn
        roc_auc = roc_auc_score(y_test, y_pred_prob)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        logger.info(f"ROC-AUC Test: {roc_auc:.4f}")
        
        # Guardar artefactos
        report_path = self.results_dir / "logit_summary.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write("       ECONOMETRIC LOGIT MODEL SUMMARY (CHURN RISK)       \n")
            f.write("="*60 + "\n\n")
            f.write(summary_str)
            f.write("\n\n" + "="*60 + "\n")
            f.write("       MACHINE LEARNING EVALUATION (SCIKIT-LEARN)         \n")
            f.write("="*60 + "\n\n")
            f.write(f"ROC-AUC Score: {roc_auc:.4f}\n\n")
            f.write("Confusion Matrix:\n")
            f.write(f"{cm}\n\n")
            f.write("Classification Report:\n")
            f.write(f"{report}\n")
            
        logger.info(f"Resultados guardados exitosamente en {report_path}")

    def run(self):
        try:
            df = self.load_data()
            X, y = self.preprocess(df)
            
            # Verificar si hay varianza en el objetivo
            if y.nunique() <= 1:
                logger.error("El target 'is_churn_risk' solo tiene 1 clase. No se puede modelar.")
                return
                
            self.train_and_evaluate(X, y)
        except Exception as e:
            logger.error(f"Fallo en pipeline de modelado: {e}")

if __name__ == "__main__":
    model = EconometricChurnModel()
    model.run()
