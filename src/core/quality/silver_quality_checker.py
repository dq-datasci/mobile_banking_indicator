import pandas as pd
import logging
from src.core.interfaces.data_quality_interface import IDataQualityChecker

logger = logging.getLogger(__name__)

class SilverQualityChecker(IDataQualityChecker):
    """
    Implementation of data quality assertions for the Silver layer.
    Cumple con SRP encargándose solo de la validación.
    Garantiza cumplimiento de ISO 27002 (Control 8.11 Data Masking).
    """

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies data quality rules:
        - Drops rows with nulls in critical fields (reviewId, score)
        - Ensures 'score' is between 1 and 5
        - Ensures PII (userName) is masked (i.e. length >= 64 if SHA-256)
        """
        if df is None or df.empty:
            return pd.DataFrame()

        initial_count = len(df)
        
        # 1. Drop critical nulls
        if "reviewId" in df.columns and "score" in df.columns:
            df = df.dropna(subset=["reviewId", "score"])
            
        # 2. Assert score range
        if "score" in df.columns:
            df = df[df["score"].between(1, 5)]
            
        # 3. Check Data Masking (ISO 27002: 8.11 y 5.34)
        if "userName" in df.columns:
            # PIIAnonymizer hashes with SHA-256, which gives 64 hex characters.
            # We drop any records that have unmasked or invalid lengths.
            invalid_masking = df[df["userName"].str.len() < 64]
            if not invalid_masking.empty:
                logger.error(f"Found {len(invalid_masking)} rows with unmasked userName. Dropping them for privacy compliance.")
                df = df[df["userName"].str.len() >= 64]
        
        final_count = len(df)
        if final_count < initial_count:
            logger.warning(f"Data quality checks removed {initial_count - final_count} invalid records.")
            
        return df
