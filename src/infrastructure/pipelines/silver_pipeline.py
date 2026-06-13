import logging
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_timestamp, input_file_name, regexp_extract

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SilverPipeline")

class SilverPipeline:
    def __init__(self, spark: SparkSession = None, bronze_dir: str = "data/bronze/", silver_dir: str = "data/silver/"):
        self.spark = spark or SparkSession.builder \
            .appName("OmniVoC-SilverPipeline") \
            .config("spark.sql.parquet.compression.codec", "snappy") \
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
            
        # Leer todos los JSONs particionados
        df = self.spark.read.option("multiline", "true").json(f"{self.bronze_dir}/*/*.json")
        
        # Extraer el nombre del banco desde la ruta del archivo usando regexp_extract
        # Ruta ejemplo: .../data/bronze/Banco_Nacional_de_Bolivia_BNB/Bille_playstore.json
        # Extraeremos el nombre del banco de la carpeta padre
        file_name_col = input_file_name()
        
        # Este regex captura la penúltima parte del path (el nombre de la carpeta del banco)
        df = df.withColumn("bank_name", regexp_extract(file_name_col, r'.*/bronze/([^/]+)/[^/]+\.json$', 1))
        
        # Limpieza básica
        # 1. Eliminar duplicados absolutos
        df_clean = df.dropDuplicates(["review_id"])
        
        # 2. Filtrar sin texto
        df_clean = df_clean.filter(col("content").isNotNull() & (col("content") != ""))
        
        # 3. Castear fechas (Pydantic las sacó como string ISO)
        if "date" in df_clean.columns:
            df_clean = df_clean.withColumn("date_parsed", to_timestamp(col("date")))
            
        # 4. Verificar schema estricto (ya lo garantizaba Pydantic, pero validamos nulls en llaves foráneas)
        df_clean = df_clean.filter(col("app_id").isNotNull())
        
        # Guardar en Silver como Parquet particionado por banco
        output_path = str(self.silver_dir / "reviews")
        logger.info(f"Guardando resultados en {output_path} particionado por banco...")
        
        df_clean.write \
            .mode("overwrite") \
            .partitionBy("bank_name") \
            .parquet(output_path)
            
        logger.info(f"Pipeline Silver completado. {df_clean.count()} registros procesados.")

if __name__ == "__main__":
    pipeline = SilverPipeline()
    pipeline.run()
