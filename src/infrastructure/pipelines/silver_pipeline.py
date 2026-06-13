import logging
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_timestamp, input_file_name, regexp_extract, concat_ws
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SilverPipeline")

class SilverPipeline:
    def __init__(self, spark: SparkSession = None, bronze_dir: str = "data/bronze/", silver_dir: str = "data/silver/"):
        self.spark = spark or SparkSession.builder \
            .appName("OmniVoC-SilverPipeline") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .master("local[*]") \
            .getOrCreate()
            
        self.bronze_dir = Path(bronze_dir)
        self.silver_dir = Path(silver_dir)
        self.silver_dir.mkdir(parents=True, exist_ok=True)
        
    def run(self):
        logger.info("Iniciando procesamiento Silver con PySpark...")
        
        if not self.bronze_dir.exists() or not list(self.bronze_dir.glob("**/*.json")):
            logger.warning("No hay datos en Bronze para procesar.")
            return
            
        # Definir esquema estricto (StructType)
        schema = StructType([
            StructField("reviewId", StringType(), True),
            StructField("userName", StringType(), True),
            StructField("userImage", StringType(), True),
            StructField("content", StringType(), True),
            StructField("score", IntegerType(), True),
            StructField("thumbsUpCount", IntegerType(), True),
            StructField("reviewCreatedVersion", StringType(), True),
            StructField("at", StringType(), True),
            StructField("replyContent", StringType(), True),
            StructField("repliedAt", StringType(), True),
            StructField("appVersion", StringType(), True)
        ])
        
        # Leer JSONs particionados con el esquema estricto
        df = self.spark.read.option("multiline", "true").schema(schema).json(f"{self.bronze_dir}/*/*.json")
        
        # Extraer el nombre del banco y app desde la ruta del archivo
        file_name_col = input_file_name()
        
        df = df.withColumn("bank_name", regexp_extract(file_name_col, r'.*/bronze/([^/]+)/[^/]+\.json$', 1))
        df = df.withColumn("app_name", regexp_extract(file_name_col, r'.*/bronze/[^/]+/(.*?)_(playstore|appstore)\.json$', 1))
        df = df.withColumn("app_id", concat_ws("_", col("bank_name"), col("app_name")))
        
        # Limpieza básica
        df_clean = df.dropDuplicates(["reviewId"])
        df_clean = df_clean.filter(col("content").isNotNull() & (col("content") != ""))
        
        # Castear fechas y renombrar
        if "at" in df_clean.columns:
            df_clean = df_clean.withColumn("date_parsed", to_timestamp(col("at")))
            
        # Renombrar score a rating para compatibilidad con Gold
        df_clean = df_clean.withColumnRenamed("score", "rating")
        df_clean = df_clean.withColumnRenamed("reviewId", "review_id")
        df_clean = df_clean.withColumnRenamed("userName", "user_name")
            
        df_clean = df_clean.filter(col("app_id").isNotNull() & (col("app_id") != ""))
        
        output_path = str(self.silver_dir / "reviews")
        logger.info(f"Guardando resultados en {output_path} particionado por banco (formato Delta)...")
        
        df_clean.write \
            .format("delta") \
            .mode("overwrite") \
            .partitionBy("bank_name") \
            .save(output_path)
            
        logger.info(f"Pipeline Silver completado. {df_clean.count()} registros procesados.")

if __name__ == "__main__":
    pipeline = SilverPipeline()
    pipeline.run()
