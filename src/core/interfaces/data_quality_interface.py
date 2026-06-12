from abc import ABC, abstractmethod
import pandas as pd

class IDataQualityChecker(ABC):
    """
    Abstract Interface for Data Quality Checkers.
    Enforces the Dependency Inversion Principle (DIP) so that high-level
    modules depend on this abstraction rather than concrete implementations.
    """

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validates the given DataFrame against quality rules.
        Should return a clean DataFrame, dropping or transforming invalid records.
        """
        pass
