from abc import ABC, abstractmethod
import pandas as pd
from typing import Any

class IAutoML(ABC):
    """
    Interface for AutoML Facades, enforcing Dependency Inversion Principle (DIP).
    """
    @abstractmethod
    def train_and_compare_baselines(self, data: pd.DataFrame, target: str) -> Any:
        """
        Trains and compares multiple baseline models and returns the best model.
        
        Args:
            data (pd.DataFrame): The dataset containing features and target.
            target (str): The name of the target column.
            
        Returns:
            Any: The trained best model object.
        """
        pass
