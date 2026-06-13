from pyspark.sql import SparkSession
from src.core.quality.silver_profiler import SilverProfilerFacade

import subprocess

def main():
    print("Iniciando Spark Session...")
    spark = SparkSession.builder \
        .appName("OmniVoC-EDA-Run") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[*]") \
        .getOrCreate()
        
    print("Cargando Silver Data desde data/silver/reviews...")
    try:
        df_silver = spark.read.format("delta").load("data/silver/reviews")
        print(f"Total de registros a analizar: {df_silver.count()}")
        
        profiler = SilverProfilerFacade(spark=spark, output_dir="docs/EDA_RESULTS")
        profiler.generate_report(df_silver)
        
        print("EDA finalizado exitosamente.")
        
        print("Compilando reporte comparativo (Quarto a PDF)...")
        import os
        env = os.environ.copy()
        env["RETICULATE_PYTHON"] = "/home/dq-datasci/micromamba/envs/omnivoc_env/bin/python"
        subprocess.run(["quarto", "render", "docs/EDA_RESULTS/comparative_analysis.qmd", "--to", "pdf"], check=True, env=env)
        print("Reporte Quarto PDF generado exitosamente.")
    except Exception as e:
        print(f"Error al ejecutar EDA: {e}")

if __name__ == "__main__":
    main()
