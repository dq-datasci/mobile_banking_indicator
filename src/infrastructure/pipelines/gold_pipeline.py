import pandas as pd
import logging
from datetime import date
from src.infrastructure.database.duckdb_singleton import DuckDBConnection
from src.core.contracts.gold_contracts import DimAppContract, FactReviewsContract

# Configurar logging para cumplir con A.8.15 Logging (ISO 27001)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GoldPipeline")

class GoldPipeline:
    def __init__(self, db_connection: DuckDBConnection = None):
        # Principio de Inversión de Dependencias (DIP) y Singleton
        self.db = db_connection or DuckDBConnection()
        self.db.connect()
        self._initialize_tables()
        
    def _initialize_tables(self):
        """Inicializa el esquema de estrella si no existe en la base de datos."""
        # Dim_App con SCD2
        self.db.get_connection().execute("""
            CREATE SEQUENCE IF NOT EXISTS seq_app_sk START 1;
            CREATE TABLE IF NOT EXISTS Dim_App (
                app_sk INTEGER PRIMARY KEY,
                app_id VARCHAR,
                app_name VARCHAR,
                category VARCHAR,
                platform VARCHAR,
                valid_from DATE,
                valid_to DATE,
                is_current BOOLEAN
            );
        """)
        
        # Fact_Reviews
        self.db.get_connection().execute("""
            CREATE TABLE IF NOT EXISTS Fact_Reviews (
                review_id VARCHAR PRIMARY KEY,
                app_sk INTEGER,
                date_sk INTEGER,
                sentiment_sk INTEGER,
                user_sk VARCHAR,
                nps_contribution DOUBLE,
                is_churn_risk BOOLEAN,
                rating INTEGER
            );
        """)
    
    def process_app_dimension(self, app_df: pd.DataFrame) -> None:
        """
        Procesa la dimensión de aplicación aplicando Slowly Changing Dimensions Tipo 2.
        """
        logger.info("Iniciando procesamiento de Dim_App con lógica SCD Tipo 2.")
        try:
            conn = self.db.get_connection()
            conn.register("incoming_apps", app_df)
            
            # Detectar cambios o nuevos registros
            changes = conn.execute("""
                SELECT i.* 
                FROM incoming_apps i
                LEFT JOIN Dim_App d ON i.app_id = d.app_id AND d.is_current = TRUE
                WHERE d.app_id IS NULL 
                   OR d.app_name != i.app_name 
                   OR d.category != i.category 
                   OR d.platform != i.platform
            """).fetchdf()
            
            if changes.empty:
                logger.info("No se detectaron cambios para Dim_App.")
                conn.unregister("incoming_apps")
                return
            
            # Cerrar registros antiguos (SCD Type 2)
            conn.execute("""
                UPDATE Dim_App 
                SET valid_to = CURRENT_DATE, is_current = FALSE
                WHERE is_current = TRUE 
                  AND app_id IN (SELECT app_id FROM incoming_apps)
                  AND (app_name != (SELECT app_name FROM incoming_apps WHERE app_id = Dim_App.app_id)
                       OR category != (SELECT category FROM incoming_apps WHERE app_id = Dim_App.app_id)
                       OR platform != (SELECT platform FROM incoming_apps WHERE app_id = Dim_App.app_id))
            """)
            
            # Insertar nuevos registros activos
            conn.execute("""
                INSERT INTO Dim_App
                SELECT 
                    nextval('seq_app_sk'),
                    app_id,
                    app_name,
                    category,
                    platform,
                    CURRENT_DATE as valid_from,
                    NULL as valid_to,
                    TRUE as is_current
                FROM incoming_apps
                WHERE app_id IN (
                    SELECT app_id FROM incoming_apps 
                    EXCEPT 
                    SELECT app_id FROM Dim_App WHERE is_current = TRUE
                )
            """)
            
            conn.unregister("incoming_apps")
            logger.info(f"Dim_App procesada con éxito. {len(changes)} registros insertados/actualizados.")
            
        except Exception as e:
            logger.error(f"Error procesando Dim_App (Posible corrupción o data inválida): {str(e)}")
            raise
            
    def process_fact_reviews(self, reviews_df: pd.DataFrame) -> None:
        """
        Procesa la tabla Fact_Reviews asignando Surrogate Keys.
        """
        logger.info("Iniciando procesamiento de Fact_Reviews.")
        try:
            conn = self.db.get_connection()
            conn.register("incoming_reviews", reviews_df)
            
            # Realizar el join con la dimensión activa
            conn.execute("""
                INSERT INTO Fact_Reviews
                SELECT 
                    r.review_id,
                    d.app_sk,
                    r.date_sk,
                    r.sentiment_sk,
                    r.user_sk,
                    r.nps_contribution,
                    r.is_churn_risk,
                    r.rating
                FROM incoming_reviews r
                JOIN Dim_App d ON r.app_id = d.app_id AND d.is_current = TRUE
                WHERE r.review_id NOT IN (SELECT review_id FROM Fact_Reviews)
            """)
            
            conn.unregister("incoming_reviews")
            logger.info("Fact_Reviews procesada con éxito.")
            
        except Exception as e:
            logger.error(f"Error procesando Fact_Reviews: {str(e)}")
            raise
