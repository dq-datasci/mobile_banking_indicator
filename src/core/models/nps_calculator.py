import os
import logging
from pathlib import Path
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NPSCalculator")

class NPSCalculator:
    def __init__(self, gold_dir: str = "data/gold/"):
        self.gold_dir = Path(gold_dir)
        self.results_dir = Path("docs/MODELS_RESULTS/")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.spark = SparkSession.builder \
            .appName("OmniVoC-NPSCalculator") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .master("local[*]") \
            .getOrCreate()

    def run(self):
        logger.info("Calculando el Net Promoter Score (NPS) desde Gold...")
        
        fact_path = str(self.gold_dir / "Fact_Reviews")
        dim_app_path = str(self.gold_dir / "Dim_App")
        
        if not os.path.exists(fact_path) or not os.path.exists(dim_app_path):
            logger.error("No se encontraron las tablas Delta de Gold.")
            return

        fact_df = self.spark.read.format("delta").load(fact_path)
        dim_app = self.spark.read.format("delta").load(dim_app_path)
        
        # Enriquecer con el nombre del banco
        df = fact_df.join(dim_app, fact_df.app_sk == dim_app.app_sk, "inner")
        
        # Clasificar Promotores, Pasivos, Detractores
        # 5 -> Promoter (1), 4-3 -> Passive (0), 2-1 -> Detractor (-1)
        df = df.withColumn(
            "nps_category",
            F.when(F.col("rating") == 5, "Promoter")
             .when(F.col("rating").isin([3, 4]), "Passive")
             .when(F.col("rating").isin([1, 2]), "Detractor")
             .otherwise("Unknown")
        )
        
        # Agregar totales por banco
        total_counts = df.groupBy("bank_name").agg(
            F.count("review_id").alias("total_reviews"),
            F.sum(F.when(F.col("nps_category") == "Promoter", 1).otherwise(0)).alias("promoters"),
            F.sum(F.when(F.col("nps_category") == "Passive", 1).otherwise(0)).alias("passives"),
            F.sum(F.when(F.col("nps_category") == "Detractor", 1).otherwise(0)).alias("detractors")
        )
        
        # Calcular % y NPS Final = %Promoters - %Detractors
        nps_df = total_counts.withColumn(
            "nps_score",
            ((F.col("promoters") / F.col("total_reviews")) - (F.col("detractors") / F.col("total_reviews"))) * 100
        )
        
        nps_df = nps_df.orderBy(F.col("nps_score").desc())
        
        # Guardar como tabla en Gold y en un reporte plano
        nps_out_path = str(self.gold_dir / "Aggr_NPS")
        nps_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(nps_out_path)
        logger.info(f"NPS guardado en {nps_out_path}")
        
        # Guardar en Pandas para generar el texto del reporte
        pandas_nps = nps_df.toPandas()
        
        report_path = self.results_dir / "nps_summary.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("="*60 + "\n")
            f.write("               REPORTE ECONOMÉTRICO DE NPS                \n")
            f.write("="*60 + "\n\n")
            f.write(pandas_nps.to_string(index=False))
            
        logger.info("Reporte plano guardado.")
        
if __name__ == "__main__":
    calc = NPSCalculator()
    calc.run()
