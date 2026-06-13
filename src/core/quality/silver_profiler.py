import os
import pandas as pd
from pathlib import Path
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from src.core.security.audit_logger import AuditLogger

try:
    from ydata_profiling import ProfileReport
except ImportError:
    ProfileReport = None


class SilverProfilerFacade:
    """
    Facade para el análisis exploratorio automático (EDA) sobre la capa Silver.
    Usa PySpark para el dataset global (evitando OOM) y ydata-profiling para un cliente muestreado.
    Cumple con el principio SRP y patrón Facade.
    """
    
    def __init__(self, spark: SparkSession = None, output_dir: str = "docs/EDA_RESULTS"):
        self.spark = spark or SparkSession.builder \
            .appName("OmniVoC-EDA") \
            .master("local[*]") \
            .getOrCreate()
            
        self.output_dir = Path(output_dir)
        self.global_dir = self.output_dir / "GLOBAL"
        self.client_dir = self.output_dir / "CLIENT_BCP"
        self.global_dir.mkdir(parents=True, exist_ok=True)
        self.client_dir.mkdir(parents=True, exist_ok=True)
        self.logger = AuditLogger()
        self.logger.info("SilverProfilerFacade", "Inicializado el generador de reportes EDA avanzados.")

    def run_global_eda_pyspark(self, df_silver):
        """
        Calcula estadísticas distribuidas usando PySpark para prevenir OOM.
        Guarda los resultados como CSVs e histogramas en docs/EDA_RESULTS/GLOBAL/
        """
        self.logger.info("SilverProfilerFacade", "Iniciando EDA global con PySpark...")
        
        row_count = df_silver.count()
        if row_count == 0:
            self.logger.warning("SilverProfilerFacade", "El DataFrame de entrada está vacío.")
            return

        # 1. Valores Nulos
        null_exprs = [F.sum(F.when(F.col(c).isNull() | (F.col(c) == ""), 1).otherwise(0)).alias(c) for c in df_silver.columns]
        nulls_df = df_silver.agg(*null_exprs).toPandas().T
        nulls_df.columns = ["Missing_Count"]
        nulls_df["Missing_Percent"] = (nulls_df["Missing_Count"] / row_count) * 100
        nulls_df.to_csv(self.global_dir / "missing_values.csv")
        
        # 2. Estadísticas Numéricas e Histogramas
        num_cols = [f.name for f in df_silver.schema.fields if f.dataType.typeName() in ["integer", "double", "float", "long"]]
        if num_cols:
            stats = df_silver.select(*num_cols).describe().toPandas()
            stats.to_csv(self.global_dir / "numeric_stats.csv", index=False)
            
            # Muestreo estratificado para gráficos (evita saturar memoria del Driver)
            sample_fraction = min(1.0, 100000.0 / float(max(row_count, 1)))
            sample_df = df_silver.select(*num_cols).sample(fraction=sample_fraction, seed=42).toPandas()
            
            # Configurar estilo visual premium
            plt.style.use('seaborn-v0_8-whitegrid')
            sns.set_palette('husl')
            
            for col in num_cols:
                plt.figure(figsize=(8, 4))
                sns.histplot(sample_df[col].dropna(), bins=30, kde=True, color='steelblue', edgecolor='white')
                plt.title(f'Distribución de {col}', fontsize=14, fontweight='bold')
                
                # Quitar bordes innecesarios
                ax = plt.gca()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
                plt.savefig(self.global_dir / f"dist_{col}.png")
                plt.close()

        # 3. Cardinalidad y Conteo de Categóricas
        cat_cols = [f.name for f in df_silver.schema.fields if f.dataType.typeName() == "string"]
        for col in cat_cols:
            top_cats = df_silver.groupBy(col).count().orderBy(F.col("count").desc()).limit(20).toPandas()
            top_cats.to_csv(self.global_dir / f"categorical_{col}.csv", index=False)

        self.logger.info("SilverProfilerFacade", "EDA global completado exitosamente.")

    def run_client_eda_ydata(self, df_silver, client_name: str = "Banco_de_Crédito_BCP"):
        """
        Ejecuta ydata-profiling sobre un subconjunto de datos (un banco específico)
        para mantener la interactividad sin quebrar la memoria.
        """
        self.logger.info("SilverProfilerFacade", f"Iniciando EDA específico para {client_name} con ydata-profiling...")
        client_df = df_silver.filter(F.col("bank_name") == client_name)
        
        client_count = client_df.count()
        if client_count == 0:
            self.logger.warning("SilverProfilerFacade", f"No se encontraron datos para {client_name}.")
            return
            
        sample_size = 50000.0
        if client_count > sample_size:
            fraction = sample_size / float(client_count)
            client_pd = client_df.sample(fraction=fraction, seed=42).toPandas()
        else:
            client_pd = client_df.toPandas()
            
        report_path = self.client_dir / "bcp_ydata_report.html"
        
        if ProfileReport is None:
            raise ImportError("ydata-profiling no está instalado.")
            
        profile = ProfileReport(client_pd, title=f"EDA Report - {client_name}", minimal=True, pool_size=1)
        profile.to_file(str(report_path))
        self.logger.info("SilverProfilerFacade", f"Reporte cliente generado en {report_path}")

    def run_global_eda_ydata_dynamic(self, df_silver):
        """
        Genera reporte interactivo para todo el dataset si su tamaño no excede MAX_YDATA_ROWS.
        """
        MAX_YDATA_ROWS = 100000
        count = df_silver.count()
        if count <= MAX_YDATA_ROWS:
            self.logger.info("SilverProfilerFacade", f"Volumen {count} <= {MAX_YDATA_ROWS}. Generando YData Profiling GLOBAL...")
            report_path = self.global_dir / "global_ydata_report.html"
            
            if ProfileReport is None:
                raise ImportError("ydata-profiling no está instalado.")
                
            global_pd = df_silver.toPandas()
            profile = ProfileReport(global_pd, title="EDA Report - GLOBAL (All Banks)", minimal=True, pool_size=1)
            profile.to_file(str(report_path))
            self.logger.info("SilverProfilerFacade", f"Reporte global generado en {report_path}")
        else:
            self.logger.info("SilverProfilerFacade", f"Volumen {count} > {MAX_YDATA_ROWS}. Se omite YData Profiling GLOBAL interactivo para evitar OOM.")

    def generate_report(self, df_silver) -> dict:
        """
        Método principal que coordina ambos enfoques (Distributed + Sampled).
        """
        self.run_global_eda_pyspark(df_silver)
        self.run_global_eda_ydata_dynamic(df_silver)
        self.run_client_eda_ydata(df_silver)
        return {
            "global_dir": str(self.global_dir),
            "client_dir": str(self.client_dir)
        }
