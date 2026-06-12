import logging
import pandas as pd
from typing import Optional
from pathlib import Path

from src.core.interfaces.database_interface import IDatabase
from src.core.interfaces.data_quality_interface import IDataQualityChecker

logger = logging.getLogger(__name__)

class SilverPipeline:
    """
    Facade for the Silver transformation pipeline.
    Reads from Bronze, applies Data Quality checks, and saves to Silver.
    """
    def __init__(self, db: IDatabase, quality_checker: IDataQualityChecker, bronze_table: str = "bronze_reviews", silver_dir: str = "data/silver"):
        self.db = db
        self.quality_checker = quality_checker
        self.bronze_table = bronze_table
        self.silver_dir = Path(silver_dir)

    def run(self) -> Optional[pd.DataFrame]:
        """
        Ejecuta el flujo del pipeline (Extract de Bronze -> Transform/Check -> Load a Silver).
        Maneja errores según directrices de DEVOPS_MLOPS_SECURITY.md.
        """
        logger.info("Starting Silver Pipeline execution...")
        try:
            # 1. Read from Bronze
            query = f"SELECT * FROM {self.bronze_table}"
            df_bronze = self.db.execute_query(query)
            
            if df_bronze is None or df_bronze.empty:
                logger.info("No data found in Bronze layer.")
                return None

            # 2. Apply Quality Checks & ISO 27002 controls
            df_silver = self.quality_checker.validate(df_bronze)
            
            # 3. Save to Silver partitioned by year/month
            if not df_silver.empty:
                self._save_partitioned(df_silver)
            else:
                logger.warning("All records were filtered out during quality checks.")
                
            logger.info("Silver Pipeline execution completed successfully.")
            return df_silver
            
        except Exception as e:
            logger.error(f"Error during Silver Pipeline execution: {str(e)}")
            raise

    def _save_partitioned(self, df: pd.DataFrame) -> None:
        """
        Saves DataFrame to Parquet partitioned by year/month.
        """
        if "at" in df.columns:
            # Ensure datetime type
            df["at"] = pd.to_datetime(df["at"], errors='coerce')
            df["year"] = df["at"].dt.year
            df["month"] = df["at"].dt.month
            
            # Drop rows where 'at' could not be parsed
            df = df.dropna(subset=["year", "month"])
            
            # Save partitioned parquet
            self.silver_dir.mkdir(parents=True, exist_ok=True)
            df.to_parquet(self.silver_dir, partition_cols=["year", "month"], existing_data_behavior="delete_matching")
            logger.info(f"Saved {len(df)} records to {self.silver_dir} partitioned by year and month.")
        else:
            logger.warning("Column 'at' not found. Saving unpartitioned.")
            self.silver_dir.mkdir(parents=True, exist_ok=True)
            df.to_parquet(self.silver_dir / "silver_data.parquet")
