import abc
from typing import List, Dict, Any

class BaseScraper(abc.ABC):
    """
    Clase abstracta base para todos los scrapers de tiendas de aplicaciones y redes sociales.
    Cumple con el Liskov Substitution Principle (LSP).
    """

    @abc.abstractmethod
    def extract_reviews(self, app_id: str, max_reviews: int = 100) -> List[Dict[str, Any]]:
        """
        Extrae reseñas de la plataforma y devuelve una lista de diccionarios crudos.
        
        Args:
            app_id (str): Identificador único de la app en la plataforma.
            max_reviews (int): Cantidad máxima de reseñas a extraer.
            
        Returns:
            List[Dict[str, Any]]: Lista de reseñas extraídas.
        """
        pass
