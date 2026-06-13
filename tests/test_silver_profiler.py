import pandas as pd
from pathlib import Path
from src.core.quality.silver_profiler import SilverProfilerFacade
from pyspark.sql import SparkSession

def test_silver_profiler_generate_report(tmp_path):
    """
    Prueba que el EDA global y el reporte cliente se generen correctamente usando PySpark.
    """
    spark = SparkSession.builder.master("local[1]").appName("Test-SilverProfiler").getOrCreate()
    data = [
        ("1", "user1", "A", 5, "Banco de Crédito (BCP)"),
        ("2", "user2", "B", 4, "Banco de Crédito (BCP)"),
        ("3", "user3", "C", 1, "Otro Banco")
    ]
    df = spark.createDataFrame(data, ["review_id", "user_name", "content", "rating", "bank_name"])
    
    profiler = SilverProfilerFacade(spark=spark, output_dir=str(tmp_path))
    
    # Mockear plt.savefig para no generar imagenes en los unit tests en CI
    import matplotlib.pyplot as plt
    original_savefig = plt.savefig
    plt.savefig = lambda *args, **kwargs: None
    
    paths = profiler.generate_report(df)
    
    plt.savefig = original_savefig
    
    assert Path(paths["global_dir"]).exists()
    assert Path(paths["client_dir"]).exists()
    assert (Path(paths["global_dir"]) / "missing_values.csv").exists()
    assert (Path(paths["global_dir"]) / "numeric_stats.csv").exists()

def test_silver_profiler_fallback(tmp_path, monkeypatch):
    """
    Prueba el manejo de errores si ydata-profiling falla o no está instalado, 
    asegurando que el proceso Global siga funcionando sin caerse.
    """
    spark = SparkSession.builder.master("local[1]").appName("Test-SilverProfiler").getOrCreate()
    data = [("1", "user1", "A", 5, "Banco de Crédito (BCP)")]
    df = spark.createDataFrame(data, ["review_id", "user_name", "content", "rating", "bank_name"])
    
    profiler = SilverProfilerFacade(spark=spark, output_dir=str(tmp_path))
    
    # Forzar que ydata-profiling no exista
    import src.core.quality.silver_profiler as sp
    monkeypatch.setattr(sp, "ProfileReport", None)
    
    profiler.generate_report(df)
    
    # El archivo del cliente no debe existir, pero el proceso PySpark Global sí
    assert Path(profiler.global_dir / "missing_values.csv").exists()
