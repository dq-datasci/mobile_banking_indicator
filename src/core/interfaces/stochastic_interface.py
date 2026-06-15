from abc import ABC, abstractmethod
import pandas as pd

class IStochasticModel(ABC):
    """
    Interface for Stochastic Mathematical Models (Markov Chains, Queuing Theory, etc.)
    Enforces Open/Closed Principle (OCP).
    """
    
    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> dict:
        """
        Calculates stochastic probabilities based on the given dataframe.
        Must return a dictionary with the specific metrics.
        """
        pass
