from src.core.interfaces.scraper_interface import BaseScraper
from src.infrastructure.extractors.playstore_scraper import PlayStoreScraper
from src.infrastructure.extractors.appstore_scraper import AppStoreScraper


class ScraperFactory:
    """
    Patrón Factory para instanciar el scraper correcto dependiendo de la fuente solicitada.
    """

    @staticmethod
    def get_scraper(source: str) -> BaseScraper:
        source_lower = source.lower()
        if source_lower == "playstore":
            return PlayStoreScraper()
        elif source_lower == "appstore":
            return AppStoreScraper(country="bo")
        else:
            raise ValueError(f"Fuente de extracción no soportada: {source}")
