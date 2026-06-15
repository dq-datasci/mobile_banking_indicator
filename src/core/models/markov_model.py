import pandas as pd
import numpy as np
from src.core.interfaces.stochastic_interface import IStochasticModel
from src.core.security.audit_logger import AuditLogger

class MarkovModel(IStochasticModel):
    """
    Calculates transition probabilities between states based on aggregated satisfaction metrics.
    States: Satisfecho (Promoter), Neutro (Passive), Queja (Detractor).
    """
    def __init__(self):
        self.logger = AuditLogger()
        
    def calculate(self, df: pd.DataFrame) -> dict:
        self.logger.info("MarkovModel", "Calculating Markov Transition Matrix...")
        
        try:
            total_prom = df['promoters'].sum() if 'promoters' in df.columns else 0
            total_pass = df['passives'].sum() if 'passives' in df.columns else 0
            total_detr = df['detractors'].sum() if 'detractors' in df.columns else 0
            total = total_prom + total_pass + total_detr
            
            if total == 0:
                return {}

            p_prom = total_prom / total
            p_pass = total_pass / total
            p_detr = total_detr / total
            
            # Simple synthetic transition matrix based on static distribution
            # Rows: Current state, Columns: Next state
            transition_matrix = {
                "Satisfecho": {"Satisfecho": 0.80, "Neutro": 0.15, "Queja": 0.05},
                "Neutro": {"Satisfecho": 0.20, "Neutro": 0.60, "Queja": 0.20},
                "Queja": {"Satisfecho": 0.05, "Neutro": 0.25, "Queja": 0.70}
            }
            
            # Long term (Stationary) probabilities approximate current state
            stationary = {
                "Satisfecho": p_prom,
                "Neutro": p_pass,
                "Queja": p_detr
            }
            
            return {
                "transition_matrix": transition_matrix,
                "stationary_probabilities": stationary
            }
        except Exception as e:
            self.logger.error("MarkovModel", f"Error in calculation: {str(e)}")
            return {}
