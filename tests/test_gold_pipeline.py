import pytest
import pandas as pd
from src.infrastructure.pipelines.gold_pipeline import GoldPipeline
from src.infrastructure.database.duckdb_singleton import DuckDBConnection

@pytest.fixture
def gold_pipeline():
    # Instanciamos una base de datos en memoria para no ensuciar datos persistentes
    db = DuckDBConnection(db_path=":memory:")
    db.connect()
    pipeline = GoldPipeline(db_connection=db)
    # Limpiamos antes de cada prueba por seguridad
    pipeline.db.get_connection().execute("DELETE FROM Fact_Reviews")
    pipeline.db.get_connection().execute("DELETE FROM Dim_App")
    yield pipeline

def test_dim_app_scd2_logic(gold_pipeline):
    """
    Verifica que la dimensión Dim_App maneje correctamente los cambios lentos (SCD Tipo 2).
    """
    # 1. Inserción Inicial
    initial_data = pd.DataFrame([{
        "app_id": "com.bank.app",
        "app_name": "Bank App v1",
        "category": "Finance",
        "platform": "Android"
    }])
    
    gold_pipeline.process_app_dimension(initial_data)
    
    res1 = gold_pipeline.db.execute_query("SELECT * FROM Dim_App")
    assert len(res1) == 1, "Debería haber 1 registro inicial"
    assert res1.iloc[0]["is_current"] == True
    assert res1.iloc[0]["app_name"] == "Bank App v1"
    
    # 2. Actualización de Atributos (SCD Tipo 2 se activa)
    updated_data = pd.DataFrame([{
        "app_id": "com.bank.app",
        "app_name": "Bank App v2", # Cambio de nombre
        "category": "Finance",
        "platform": "Android"
    }])
    
    gold_pipeline.process_app_dimension(updated_data)
    
    res2 = gold_pipeline.db.execute_query("SELECT * FROM Dim_App ORDER BY app_sk")
    assert len(res2) == 2, "Debería haber 2 registros ahora (uno activo, uno inactivo)"
    
    # El primer registro debería estar inactivo (is_current = False)
    assert res2.iloc[0]["is_current"] == False
    assert res2.iloc[0]["valid_to"] is not None
    
    # El segundo registro debería estar activo (is_current = True)
    assert res2.iloc[1]["is_current"] == True
    assert res2.iloc[1]["app_name"] == "Bank App v2"
    assert pd.isna(res2.iloc[1]["valid_to"])

def test_fact_reviews_insertion(gold_pipeline):
    """
    Verifica que la tabla de hechos Fact_Reviews obtenga la clave subrogada (Surrogate Key) correcta de Dim_App.
    """
    # Preparar dimensión
    app_data = pd.DataFrame([{
        "app_id": "com.test.app",
        "app_name": "Test App",
        "category": "Tools",
        "platform": "iOS"
    }])
    gold_pipeline.process_app_dimension(app_data)
    
    # Preparar tabla de hechos (cruda desde Silver)
    reviews_data = pd.DataFrame([{
        "review_id": "REV-001",
        "app_id": "com.test.app", # Natural Key
        "date_sk": 20260612,
        "sentiment_sk": 1,
        "user_sk": "hash_xyz_123", # PII ya hasheada (ISO 27001)
        "nps_contribution": 100.0,
        "is_churn_risk": False,
        "rating": 5
    }])
    
    gold_pipeline.process_fact_reviews(reviews_data)
    
    # Verificar inserción
    res = gold_pipeline.db.execute_query("SELECT * FROM Fact_Reviews")
    assert len(res) == 1
    assert res.iloc[0]["review_id"] == "REV-001"
    
    app_sk = gold_pipeline.db.execute_query("SELECT app_sk FROM Dim_App WHERE app_id = 'com.test.app'").iloc[0]["app_sk"]
    assert res.iloc[0]["app_sk"] == app_sk # Surrogate Key generado dinámicamente
