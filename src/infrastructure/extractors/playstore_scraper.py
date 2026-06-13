import time
import hashlib
from typing import List, Dict, Any
from google_play_scraper import reviews, Sort
from src.core.interfaces.scraper_interface import BaseScraper
import os
import pandas as pd


class PlayStoreScraper(BaseScraper):
    """
    Implementación del scraper para Google Play Store usando google_play_scraper.
    """

    def _hash_username(self, username: str) -> str:
        if not username:
            return "Anonymous"
        return hashlib.sha256(username.encode('utf-8')).hexdigest()

    def extract_reviews(
        self, app_id: str, max_reviews: int = 100
    ) -> List[Dict[str, Any]]:
        all_reviews = []
        continuation_token = None
        retries = 3
        backoff_factor = 2

        self.logger.info(self.__class__.__name__, f"Iniciando extracción Play Store para {app_id}")

        while len(all_reviews) < max_reviews:
            try:
                # Extraemos en bloques de 100 (límite de la librería/API)
                count = min(100, max_reviews - len(all_reviews))
                result, continuation_token = reviews(
                    app_id,
                    lang="es",
                    country="bo",
                    sort=Sort.NEWEST,
                    count=count,
                    continuation_token=continuation_token,
                )
                
                if not result:
                    self.logger.info(self.__class__.__name__, f"No se encontraron más reseñas para {app_id}.")
                    break
                    
                all_reviews.extend(result)

                if not continuation_token:
                    break

                time.sleep(1)  # delay básico para evitar ban

            except Exception as e:
                self.logger.error(self.__class__.__name__, f"Error extrayendo de Play Store: {e}")
                if retries > 0:
                    wait_time = backoff_factor ** (4 - retries)
                    self.logger.info(self.__class__.__name__, f"Reintentando en {wait_time} segundos...")
                    time.sleep(wait_time)
                    retries -= 1
                else:
                    self.logger.error(self.__class__.__name__, "Se acabaron los reintentos para Play Store.")
                    break

        # Garantizar Idempotencia y Hashear Usernames por Privacidad
        unique_reviews = {r["reviewId"]: r for r in all_reviews}.values()
        unique_list = list(unique_reviews)[:max_reviews]
        
        for rev in unique_list:
            if "userName" in rev and rev["userName"]:
                rev["userName"] = self._hash_username(rev["userName"])

        return unique_list

    def save_to_bronze(self, app_id: str, data: List[Dict[str, Any]]):
        """
        Guarda los datos en la capa Bronze en formato Parquet
        """
        bronze_dir = "data/bronze/playstore"
        os.makedirs(bronze_dir, exist_ok=True)

        if not data:
            self.logger.warning(self.__class__.__name__, "No hay datos para guardar.")
            return

        df = pd.DataFrame(data)
        # Convertimos las columnas datetime porque parquet es estricto
        if "at" in df.columns:
            df["at"] = pd.to_datetime(df["at"])
        if "repliedAt" in df.columns:
            df["repliedAt"] = pd.to_datetime(df["repliedAt"])

        filename = os.path.join(bronze_dir, f"{app_id}_raw.parquet")
        df.to_parquet(filename, index=False)
        self.logger.info(self.__class__.__name__, f"Datos guardados en {filename}")
