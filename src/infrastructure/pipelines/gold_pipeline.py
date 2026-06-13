import logging
from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_date, when, monotonically_increasing_id
from pyspark.sql.window import Window

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GoldPipeline")

class GoldPipeline:
    def __init__(self, spark: SparkSession = None, silver_dir: str = "data/silver/reviews/", gold_dir: str = "data/gold/"):
        self.spark = spark or SparkSession.builder \
            .appName("OmniVoC-GoldPipeline") \
            .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .master("local[*]") \
            .getOrCreate()
            
        self.silver_dir = Path(silver_dir)
        self.gold_dir = Path(gold_dir)
        self.gold_dir.mkdir(parents=True, exist_ok=True)
        
    def process_app_dimension(self, df):
        """
        Extrae y procesa la dimensión de aplicación usando SCD Tipo 2 real con DeltaTable.merge()
        """
        logger.info("Procesando Dim_App con SCD Tipo 2...")
        dim_app_path = str(self.gold_dir / "Dim_App")
        
        # Extraer apps únicas del batch
        new_apps = df.select("app_id", "app_name", "bank_name").distinct()
        
        from delta.tables import DeltaTable
        
        if DeltaTable.isDeltaTable(self.spark, dim_app_path):
            target_table = DeltaTable.forPath(self.spark, dim_app_path)
            target_df = target_table.toDF()
            
            # Identificar filas que existen y han cambiado en algo (SCD2)
            changed_df = new_apps.join(target_df, "app_id") \
                .filter(col("is_current") == True) \
                .filter((new_apps.app_name != target_df.app_name) | (new_apps.bank_name != target_df.bank_name)) \
                .select(new_apps.app_id, new_apps.app_name, new_apps.bank_name)
                
            # Identificar filas totalmente nuevas
            new_only_df = new_apps.join(target_df, "app_id", "leftanti")
            
            # Filas a insertar (is_current=True)
            inserts_df = changed_df.unionByName(new_only_df)
            
            if inserts_df.count() > 0:
                inserts_df = inserts_df.withColumn("app_sk", monotonically_increasing_id())
                inserts_df = inserts_df.withColumn("valid_from", current_date())
                inserts_df = inserts_df.withColumn("valid_to", lit(None).cast("date"))
                inserts_df = inserts_df.withColumn("is_current", lit(True))
                
                # Crear dataframe para el merge (SCD2 standard con Delta)
                update_rows = changed_df.withColumn("mergeKey", col("app_id"))
                insert_rows = inserts_df.withColumn("mergeKey", lit(None).cast("string"))
                
                # Unir updates (que cerrarán los registros antiguos) e inserts (que crearán los nuevos)
                staged_updates = update_rows.select("mergeKey", "app_id", "app_name", "bank_name") \
                    .withColumn("app_sk", lit(None).cast("long")) \
                    .withColumn("valid_from", lit(None).cast("date")) \
                    .withColumn("valid_to", lit(None).cast("date")) \
                    .withColumn("is_current", lit(None).cast("boolean")) \
                    .unionByName(insert_rows)
                    
                logger.info("Ejecutando MERGE para SCD Tipo 2...")
                target_table.alias("target").merge(
                    staged_updates.alias("source"),
                    "target.app_id = source.mergeKey AND target.is_current = true"
                ).whenMatchedUpdate(
                    set = {
                        "is_current": lit(False),
                        "valid_to": current_date()
                    }
                ).whenNotMatchedInsert(
                    values = {
                        "app_sk": "source.app_sk",
                        "app_id": "source.app_id",
                        "app_name": "source.app_name",
                        "bank_name": "source.bank_name",
                        "valid_from": "source.valid_from",
                        "valid_to": "source.valid_to",
                        "is_current": "source.is_current"
                    }
                ).execute()
        else:
            # Carga inicial
            new_apps = new_apps.withColumn("app_sk", monotonically_increasing_id())
            new_apps = new_apps.withColumn("valid_from", current_date())
            new_apps = new_apps.withColumn("valid_to", lit(None).cast("date"))
            new_apps = new_apps.withColumn("is_current", lit(True))
            
            logger.info(f"Carga inicial de Dim_App en {dim_app_path} (Delta)")
            new_apps.write.format("delta").mode("overwrite").save(dim_app_path)
            
        # Retornar las dimensiones actuales activas
        return self.spark.read.format("delta").load(dim_app_path).filter(col("is_current") == True)

    def process_fact_reviews(self, df, dim_app):
        """
        Procesa la tabla Fact_Reviews uniendo con Dim_App para obtener Surrogate Keys.
        """
        logger.info("Procesando Fact_Reviews...")
        fact_path = str(self.gold_dir / "Fact_Reviews")
        
        # Join con la dimensión para obtener app_sk
        fact_df = df.join(dim_app, on="app_id", how="left")
        
        # Seleccionar y renombrar columnas para la tabla de hechos
        # Asumimos que sentiment_score fue calculado, si no, lo dejamos null temporalmente
        if "sentiment_score" not in fact_df.columns:
            fact_df = fact_df.withColumn("sentiment_score", lit(None).cast("double"))
            
        if "rating" not in fact_df.columns:
            fact_df = fact_df.withColumn("rating", lit(None).cast("int"))

        fact_df = fact_df.select(
            col("review_id"),
            col("app_sk"),
            col("date_parsed").alias("review_date"),
            col("rating"),
            col("sentiment_score"),
            col("user_name").alias("user_hash") # asumiendo que el Anonymizer ya lo procesó
        )
        
        logger.info(f"Guardando Fact_Reviews en {fact_path} (Delta)")
        fact_df.write.format("delta").mode("overwrite").save(fact_path)
        return fact_df

    def run(self):
        logger.info("Iniciando procesamiento Gold con PySpark...")
        if not self.silver_dir.exists():
            logger.warning("No hay datos en Silver para procesar.")
            return
            
        # 1. Leer Silver (formato Delta)
        df_silver = self.spark.read.format("delta").load(str(self.silver_dir))
        
        # 2. Procesar Dimensiones
        dim_app = self.process_app_dimension(df_silver)
        
        # 3. Procesar Hechos
        self.process_fact_reviews(df_silver, dim_app)
        
        logger.info("Pipeline Gold completado.")

if __name__ == "__main__":
    pipeline = GoldPipeline()
    pipeline.run()
