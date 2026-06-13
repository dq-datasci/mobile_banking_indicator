import json
import logging
import time
import os
from pathlib import Path
from src.infrastructure.extractors.scraper_factory import ScraperFactory
from src.core.security.anonymizer import PIIAnonymizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MassiveExtractor")

class MassiveExtractor:
    def __init__(self, config_path: str = "src/core/config/app_targets.json", output_dir: str = "data/bronze/"):
        self.config_path = config_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.anonymizer = PIIAnonymizer()
        
    def run(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        bancos = config.get("bancos", [])
        
        playstore = ScraperFactory.get_scraper("playstore")
        appstore = ScraperFactory.get_scraper("appstore")
        
        for banco in bancos:
            banco_name = banco["nombre"].replace(" ", "_").replace("(", "").replace(")", "")
            banco_dir = self.output_dir / banco_name
            banco_dir.mkdir(parents=True, exist_ok=True)
            
            for app in banco.get("apps", []):
                app_name = app["nombre"].replace(" ", "_")
                play_id = app.get("playstore_id")
                app_id = app.get("appstore_id")
                
                # Scraping PlayStore
                if play_id and play_id != "":
                    try:
                        logger.info(f"Scraping PlayStore for {banco_name} - {app_name} ({play_id})")
                        reviews = playstore.extract_reviews(app_id=play_id, max_reviews=100) # Mock limit for MVP
                        if reviews:
                            out_file = banco_dir / f"{app_name}_playstore.json"
                            with open(out_file, "w", encoding="utf-8") as out:
                                json.dump([r.model_dump() for r in reviews], out, ensure_ascii=False)
                    except Exception as e:
                        logger.error(f"Error scraping PlayStore {play_id}: {e}")
                        
                # Graceful degradation - Rate Limit Wait
                time.sleep(2)
                
                # Scraping AppStore
                if app_id and app_id != "":
                    try:
                        logger.info(f"Scraping AppStore for {banco_name} - {app_name} ({app_id})")
                        reviews = appstore.extract_reviews(app_id=app_id, max_reviews=100) # Mock limit for MVP
                        if reviews:
                            out_file = banco_dir / f"{app_name}_appstore.json"
                            with open(out_file, "w", encoding="utf-8") as out:
                                json.dump([r.model_dump() for r in reviews], out, ensure_ascii=False)
                    except Exception as e:
                        logger.error(f"Error scraping AppStore {app_id}: {e}")
                        
                # Wait between apps
                time.sleep(2)

if __name__ == "__main__":
    extractor = MassiveExtractor()
    extractor.run()
