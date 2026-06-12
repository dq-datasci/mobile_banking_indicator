from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Dimensiones (Dimensions)
# ---------------------------------------------------------

class DimAppContract(BaseModel):
    """
    Dimensión de la Aplicación con SCD Tipo 2
    """
    app_sk: int = Field(..., description="Surrogate Key autoincremental")
    app_id: str = Field(..., description="Natural Key (Bundle ID)")
    app_name: str = Field(..., description="Nombre de la aplicación")
    category: Optional[str] = Field(None, description="Categoría en la tienda")
    platform: str = Field(..., description="Plataforma (Android, iOS)")
    valid_from: date = Field(..., description="Fecha de inicio de vigencia SCD2")
    valid_to: Optional[date] = Field(None, description="Fecha de fin de vigencia SCD2")
    is_current: bool = Field(True, description="Flag activo SCD2")


class DimDateContract(BaseModel):
    """
    Dimensión de Tiempo
    """
    date_sk: int = Field(..., description="Surrogate Key Ej: 20260611")
    full_date: date = Field(..., description="Fecha completa")
    year: int = Field(..., description="Año")
    month: int = Field(..., description="Mes")
    day: int = Field(..., description="Día")
    day_of_week: str = Field(..., description="Día de la semana")
    is_weekend: bool = Field(..., description="Es fin de semana")


class DimSentimentContract(BaseModel):
    """
    Dimensión de Sentimiento (Generada por Modelos NLP)
    """
    sentiment_sk: int = Field(..., description="Surrogate Key autoincremental")
    sentiment_label: str = Field(..., description="Positivo, Neutral, Negativo")
    confidence_score_avg: float = Field(..., description="Confianza promedio del modelo")


class DimUserContract(BaseModel):
    """
    Dimensión de Usuario (Anonimizada ISO 27001)
    """
    user_sk: str = Field(..., description="Hash SHA-256 del usuario (Privacy by Design)")
    location_proxy: Optional[str] = Field(None, description="Ubicación inferida")
    is_verified: bool = Field(False, description="Usuario verificado")

# ---------------------------------------------------------
# Tabla de Hechos (Fact Table)
# ---------------------------------------------------------

class FactReviewsContract(BaseModel):
    """
    Tabla de hechos principal: Reseñas
    """
    review_id: str = Field(..., description="ID único de la reseña")
    app_sk: int = Field(..., description="Surrogate Key a Dim_App")
    date_sk: int = Field(..., description="Surrogate Key a Dim_Date")
    sentiment_sk: Optional[int] = Field(None, description="Surrogate Key a Dim_Sentiment")
    user_sk: str = Field(..., description="Surrogate Key a Dim_User")
    nps_contribution: Optional[float] = Field(None, description="Contribución al NPS (Promotor=100, Detractor=-100)")
    is_churn_risk: Optional[bool] = Field(None, description="Riesgo de fuga (Churn) calculado")
    rating: int = Field(..., ge=1, le=5, description="Puntuación en estrellas (1 a 5)")
