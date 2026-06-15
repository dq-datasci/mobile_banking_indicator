import os
import pandas as pd
from pathlib import Path
from src.use_cases.automl_facade import AutoMLFacade
from pyspark.sql import SparkSession
from pycaret.classification import save_model

def main():
    print("Iniciando Entrenamiento AutoML con PyCaret...")
    
    spark = SparkSession.builder \
        .appName("OmniVoC-AutoML") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[*]") \
        .getOrCreate()
        
    gold_path = "data/gold/Fact_Reviews"
    if not os.path.exists(gold_path):
        print("La capa Gold no existe. Corre 'python main.py run-gold' primero.")
        return
        
    print("Cargando datos Gold...")
    df_spark = spark.read.format("delta").load(gold_path)
    df = df_spark.toPandas()
    
    features = ['content_length', 'hour_of_day', 'has_bank_reply', 'is_churn_risk']
    df_model = df[features].dropna()
    df_model['content_length'] = df_model['content_length'].fillna(0).astype(int)
    df_model['hour_of_day'] = df_model['hour_of_day'].fillna(12).astype(int)
    df_model['has_bank_reply'] = df_model['has_bank_reply'].astype(int)
    df_model['is_churn_risk'] = df_model['is_churn_risk'].astype(int)
    
    if len(df_model) < 20 or df_model['is_churn_risk'].nunique() < 2:
        print("Datos insuficientes o varianza nula para ML.")
        return
        
    df_model = df_model.sample(min(len(df_model), 2000), random_state=42)
    
    automl = AutoMLFacade()
    print("Ejecutando PyCaret...")
    best_model, metrics = automl.train_and_compare_baselines(data=df_model, target='is_churn_risk')
    
    results_dir = Path("docs/MODELS_RESULTS")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    metrics.to_csv(results_dir / "pycaret_metrics.csv", index=False)
    save_model(best_model, str(results_dir / 'best_churn_model'))
    print("Métricas de AutoML y modelo guardados exitosamente en docs/MODELS_RESULTS")

if __name__ == "__main__":
    main()
