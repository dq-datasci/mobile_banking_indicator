import pytest
import pandas as pd
from pathlib import Path
from pyspark.sql import SparkSession
from src.infrastructure.pipelines.silver_pipeline import SilverPipeline
import json

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .appName("OmniVoC-Test-Silver") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.0.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def silver_pipeline(spark, tmp_path):
    bronze_dir = tmp_path / "bronze"
    silver_dir = tmp_path / "silver"
    pipeline = SilverPipeline(spark=spark, bronze_dir=str(bronze_dir), silver_dir=str(silver_dir))
    return pipeline

def test_silver_pipeline_processing(silver_pipeline, spark):
    """
    Verifica que el pipeline Silver limpie, castee fechas y extraiga el app_id a partir de la ruta.
    """
    # Preparar datos crudos simulados en Bronze
    banco_dir = silver_pipeline.bronze_dir / "Banco_Prueba"
    banco_dir.mkdir(parents=True)
    
    # Simular JSON de PlayStore
    raw_data = [
        {
            "reviewId": "R-1",
            "userName": "hash1",
            "content": "Muy buena app",
            "score": 5,
            "at": "2026-06-12T10:00:00"
        },
        {
            "reviewId": "R-2",
            "userName": "hash2",
            "content": "", # Debería ser filtrado
            "score": 1,
            "at": "2026-06-11T09:00:00"
        }
    ]
    
    file_path = banco_dir / "AppTest_playstore.json"
    with open(file_path, "w") as f:
        json.dump(raw_data, f)
        
    # Ejecutar pipeline
    silver_pipeline.run()
    
    # Leer el resultado Delta particionado
    res = spark.read.format("delta").load(str(silver_pipeline.silver_dir / "reviews")).toPandas()
    
    assert len(res) == 1, "Debería haber 1 solo registro válido (filtró el contenido vacío)"
    
    row = res.iloc[0]
    assert row["review_id"] == "R-1"
    assert row["rating"] == 5
    assert row["user_name"] == "hash1"
    assert row["bank_name"] == "Banco_Prueba"
    assert row["app_name"] == "AppTest"
    assert row["app_id"] == "Banco_Prueba_AppTest"
    assert not pd.isna(row["date_parsed"])
