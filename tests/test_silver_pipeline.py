import pytest
import pandas as pd
import numpy as np
from src.core.quality.silver_quality_checker import SilverQualityChecker

def test_silver_quality_checker_validates_correctly():
    checker = SilverQualityChecker()
    
    # Crea un DataFrame de prueba con varios casos borde
    data = {
        "reviewId": ["1", "2", None, "4", "5", "6"],
        "userName": [
            "a" * 64,                  # Válido (hasheado)
            "b" * 64,                  # Válido (hasheado)
            "c" * 64,                  # Nulo en ID, se debe eliminar
            "short_name",              # Inválido (no hasheado)
            "d" * 64,                  # Nulo en score, se debe eliminar
            "e" * 64                   # Score fuera de rango (6), se debe eliminar
        ],
        "score": [5, 1, 4, 3, np.nan, 6]
    }
    df = pd.DataFrame(data)
    
    clean_df = checker.validate(df)
    
    # Aserciones
    # Debería quedar solo la fila 1 y 2
    assert len(clean_df) == 2, f"Se esperaban 2 filas, pero quedaron {len(clean_df)}"
    
    # Comprobar que las filas correctas sobrevivieron
    valid_ids = clean_df["reviewId"].tolist()
    assert "1" in valid_ids
    assert "2" in valid_ids
    
    # Comprobar que no hay nulos en campos críticos
    assert clean_df["reviewId"].isnull().sum() == 0
    assert clean_df["score"].isnull().sum() == 0
    
    # Comprobar que todos los usernames tienen largo >= 64
    assert (clean_df["userName"].str.len() >= 64).all()
    
    # Comprobar que todos los scores están entre 1 y 5
    assert clean_df["score"].between(1, 5).all()

def test_silver_quality_checker_empty_df():
    checker = SilverQualityChecker()
    df = pd.DataFrame()
    clean_df = checker.validate(df)
    assert clean_df.empty
