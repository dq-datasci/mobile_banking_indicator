import pandas as pd
from pycaret.classification import setup, compare_models, pull
from src.core.interfaces.automl_interface import IAutoML
from src.core.security.audit_logger import AuditLogger

class AutoMLFacade(IAutoML):
    """
    Facade for PyCaret and MLflow, simplifying model comparison and logging.
    Enforces the Facade Pattern and ensures tracking through MLflow.
    """
    def __init__(self, experiment_name: str = "churn_baseline_experiment"):
        self.experiment_name = experiment_name
        self.logger = AuditLogger()
        
    def train_and_compare_baselines(self, data: pd.DataFrame, target: str):
        self.logger.info("AutoMLFacade", f"Starting PyCaret setup for experiment: {self.experiment_name}")
        
        try:
            # Configurar PyCaret con tracking automático en MLflow
            # log_experiment=True hace el autolog híbrido (métricas, hiperparámetros, artifacts)
            setup(
                data=data,
                target=target,
                session_id=42, # Para reproducibilidad
                log_experiment=True,
                experiment_name=self.experiment_name,
                verbose=False # Mantener los logs limpios
            )
            
            self.logger.info("AutoMLFacade", "Comparing baseline models...")
            # Entrenar y comparar modelos. Devuelve el mejor modelo
            best_model = compare_models(verbose=False)
            
            # Obtener el DataFrame con las métricas comparadas
            metrics_df = pull()
            
            self.logger.info("AutoMLFacade", "AutoML Baseline comparison completed successfully.")
            return best_model, metrics_df
            
        except Exception as e:
            self.logger.error("AutoMLFacade", f"Error during AutoML execution: {str(e)}")
            # Elevar excepción para que el orquestador lo maneje como INCIDENTE (Swarming)
            raise e
