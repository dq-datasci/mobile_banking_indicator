import pytest
import pandas as pd
from pathlib import Path
from src.core.quality.silver_profiler import SilverProfilerFacade

def test_silver_profiler_generate_report(tmp_path):
    """
    Prueba que el reporte de perfilamiento se genere correctamente
    cuando ydata-profiling está instalado.
    """
    data = {"col1": [1, 2, 3], "col2": ["A", "B", "C"]}
    df = pd.DataFrame(data)
    
    profiler = SilverProfilerFacade(output_dir=str(tmp_path))
    
    output_file = profiler.generate_report(df, report_name="test_profile.html")
    
    assert Path(output_file).exists()
    assert output_file.endswith(".html")

def test_silver_profiler_fallback(tmp_path, monkeypatch):
    """
    Prueba el mecanismo de degradación elegante (Fallback).
    Simula que ydata-profiling falla o no está instalado, 
    y verifica que se genere un reporte '_fallback.html' mediante pandas.
    """
    data = {"col1": [1, 2, 3], "col2": ["A", "B", "C"]}
    df = pd.DataFrame(data)
    
    profiler = SilverProfilerFacade(output_dir=str(tmp_path))
    
    import src.core.quality.silver_profiler as sp
    monkeypatch.setattr(sp, "ProfileReport", None)
    
    output_file = profiler.generate_report(df, report_name="test_profile.html")
    
    assert Path(output_file).exists()
    assert "fallback" in output_file
