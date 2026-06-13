import pandas as pd
from src.core.interfaces.stochastic_interface import IStochasticModel
from src.core.security.audit_logger import AuditLogger

class QueuingModel(IStochasticModel):
    """
    Calculates Queuing Theory metrics (M/M/1 model) to estimate Customer Service bottlenecks.
    Lambda: Arrival rate of complaints (Reviews per hour).
    Mu: Service rate (Bank replies per hour).
    """
    def __init__(self):
        self.logger = AuditLogger()
        
    def calculate(self, df: pd.DataFrame) -> dict:
        self.logger.info("QueuingModel", "Calculating Queuing Theory metrics (M/M/1)...")
        
        try:
            total_reviews = df['total_reviews'].sum() if 'total_reviews' in df.columns else 0
            
            days = 30
            lambda_rate = (total_reviews / days) / 24.0 # arrivals per hour
            
            mu_rate = 2.0 
            
            if lambda_rate > mu_rate:
                mu_rate = lambda_rate * 1.1 
            
            rho = lambda_rate / mu_rate if mu_rate > 0 else 1.0
            
            w_time = 1 / (mu_rate - lambda_rate) if (mu_rate - lambda_rate) > 0 else float('inf')
            lq = (rho ** 2) / (1 - rho) if rho < 1 else float('inf')
            
            return {
                "lambda_arrivals_per_hour": round(lambda_rate, 2),
                "mu_service_per_hour": round(mu_rate, 2),
                "rho_saturation_prob": round(rho, 2),
                "w_expected_wait_hours": round(w_time, 2),
                "lq_queue_length": round(lq, 2)
            }
        except Exception as e:
            self.logger.error("QueuingModel", f"Error in calculation: {str(e)}")
            return {}
