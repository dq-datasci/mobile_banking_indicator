import time
import logging
import os
import pandas as pd
from typing import List, Dict, Any
from app_store_scraper import AppStore
from src.core.interfaces.scraper_interface import BaseScraper

logger = logging.getLogger(__name__)

class AppStoreScraper(BaseScraper):
    """
    Implementación del scraper para Apple App Store usando app_store_scraper.
    """

    def __init__(self, country: str = 'co'):
        self.country = country

    def extract_reviews(self, app_name: str, app_id: int, max_reviews: int = 100) -> List[Dict[str, Any]]:
        # La librería AppStoreScraper requiere nombre e ID. 
        # Modificamos la firma usando app_id como el ID numérico y usamos kwargs si es necesario.
        # Para cumplir con el interface, esperamos app_id como un string compuesto "app_name,app_id"
        # O si el usuario nos pasa "app_name,app_id"
        try:
            name, identifier = app_id.split(",")
            identifier = int(identifier)
        except Exception:
            raise ValueError("Para App Store, app_id debe ser el formato 'app_name,app_id' numérico. Ej: 'nequi,1302266602'")
            
        app = AppStore(country=self.country, app_name=name, app_id=identifier)
        
        retries = 3
        backoff_factor = 2
        
        logger.info(f"Iniciando extracción App Store para {name}")
        
        while retries > 0:
            try:
                app.review(how_many=max_reviews)
                break
            except Exception as e:
                logger.error(f"Error extrayendo de App Store: {e}")
                wait_time = backoff_factor ** (4 - retries)
                logger.info(f"Reintentando en {wait_time} segundos...")
                time.sleep(wait_time)
                retries -= 1
        
        if not app.reviews:
            return []
            
        # Garantizar Idempotencia
        all_reviews = app.reviews
        unique_reviews = {str(r.get('id', i)): r for i, r in enumerate(all_reviews)}.values()
        unique_list = list(unique_reviews)[:max_reviews]
        
        return unique_list

    def save_to_bronze(self, app_id: str, data: List[Dict[str, Any]]):
        """
        Guarda los datos en la capa Bronze en formato Parquet
        """
        bronze_dir = "data/bronze/appstore"
        os.makedirs(bronze_dir, exist_ok=True)
        
        if not data:
            logger.warning("No hay datos para guardar.")
            return
            
        df = pd.DataFrame(data)
        
        # Convertir fechas
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            
        name = app_id.split(",")[0]
        filename = os.path.join(bronze_dir, f"{name}_raw.parquet")
        df.to_parquet(filename, index=False)
        logger.info(f"Datos guardados en {filename}")
