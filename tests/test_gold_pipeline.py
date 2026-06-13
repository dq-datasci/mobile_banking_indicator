import pytest
import pandas as pd
from pathlib import Path
from pyspark.sql import SparkSession
from src.infrastructure.pipelines.gold_pipeline import GoldPipeline

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .appName("OmniVoC-Test") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.0.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def gold_pipeline(spark, tmp_path):
    silver_dir = tmp_path / "silver"
    gold_dir = tmp_path / "gold"
    pipeline = GoldPipeline(spark=spark, silver_dir=str(silver_dir), gold_dir=str(gold_dir))
    return pipeline

def test_dim_app_scd2_logic(gold_pipeline, spark):
    """
    Verifica que la dimensión Dim_App maneje correctamente los cambios lentos (SCD Tipo 2) usando DeltaTable.merge.
    """
    initial_data = pd.DataFrame([{
        "app_id": "com.bank.app",
        "app_name": "Bank App v1",
        "bank_name": "Test Bank"
    }])
    df_initial = spark.createDataFrame(initial_data)
    
    gold_pipeline.process_app_dimension(df_initial)
    
    res1 = spark.read.format("delta").load(str(gold_pipeline.gold_dir / "Dim_App")).toPandas()
    assert len(res1) == 1, "Debería haber 1 registro inicial"
    assert res1.iloc[0]["is_current"] == True
    assert res1.iloc[0]["app_name"] == "Bank App v1"
    
    updated_data = pd.DataFrame([{
        "app_id": "com.bank.app",
        "app_name": "Bank App v2", # Cambio de nombre
        "bank_name": "Test Bank"
    }])
    df_updated = spark.createDataFrame(updated_data)
    
    gold_pipeline.process_app_dimension(df_updated)
    
    res2 = spark.read.format("delta").load(str(gold_pipeline.gold_dir / "Dim_App")).toPandas()
    res2 = res2.sort_values(by="app_name").reset_index(drop=True)
    assert len(res2) == 2, "Debería haber 2 registros ahora (uno activo, uno inactivo)"
    
    assert res2.iloc[0]["app_name"] == "Bank App v1"
    assert res2.iloc[0]["is_current"] == False
    assert res2.iloc[0]["valid_to"] is not None
    
    assert res2.iloc[1]["app_name"] == "Bank App v2"
    assert res2.iloc[1]["is_current"] == True
    assert pd.isna(res2.iloc[1]["valid_to"])

def test_fact_reviews_insertion(gold_pipeline, spark):
    """
    Verifica que la tabla de hechos Fact_Reviews obtenga la clave subrogada correcta de Dim_App y renombre correctamente columnas.
    """
    app_data = pd.DataFrame([{
        "app_id": "com.test.app",
        "app_name": "Test App",
        "bank_name": "Test Bank"
    }])
    df_app = spark.createDataFrame(app_data)
    dim_app = gold_pipeline.process_app_dimension(df_app)
    
    reviews_data = pd.DataFrame([{
        "review_id": "REV-001",
        "app_id": "com.test.app",
        "date_parsed": pd.Timestamp('2026-06-12'),
        "rating": 5,
        "sentiment_score": 1.0,
        "user_name": "hash_xyz_123"
    }])
    df_reviews = spark.createDataFrame(reviews_data)
    
    gold_pipeline.process_fact_reviews(df_reviews, dim_app)
    
    res = spark.read.format("delta").load(str(gold_pipeline.gold_dir / "Fact_Reviews")).toPandas()
    assert len(res) == 1
    assert res.iloc[0]["review_id"] == "REV-001"
    assert res.iloc[0]["user_hash"] == "hash_xyz_123"
    assert res.iloc[0]["app_sk"] is not None
