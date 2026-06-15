import logging
from transformers import pipeline

logger = logging.getLogger("NLPFacade")

class NLPFacade:
    """
    Facade para inferencia NLP (Clasificación de Sentimiento y Tópicos).
    Aplica el patrón Facade para ocultar la complejidad de la librería transformers.
    """
    def __init__(self, model_name: str = "finiteautomata/beto-sentiment-analysis"):
        logger.info(f"Inicializando NLPFacade con el modelo: {model_name}")
        try:
            self.sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
        except Exception as e:
            logger.error(f"Error cargando el modelo NLP: {e}")
            self.sentiment_pipeline = None

    def analyze_sentiment(self, text: str) -> str:
        """
        Devuelve 'Positivo', 'Neutral' o 'Negativo'.
        """
        if not self.sentiment_pipeline or not isinstance(text, str) or not text.strip():
            return "Neutral" # Fallback
            
        try:
            # HuggingFace pipeline corta textos largos
            result = self.sentiment_pipeline(text[:512])[0]
            label = result['label']
            if label == 'POS':
                return "Positivo"
            elif label == 'NEG':
                return "Negativo"
            else:
                return "Neutral"
        except Exception as e:
            logger.warning(f"Error analizando texto '{text[:30]}...': {e}")
            return "Neutral"
