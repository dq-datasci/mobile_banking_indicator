from abc import ABC, abstractmethod
import pandas as pd


class IDatabase(ABC):
    """
    Abstract Interface for Database connections.
    Enforces the Dependency Inversion Principle (DIP) so that high-level
    modules depend on this abstraction rather than concrete implementations like DuckDB.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establishes connection to the database"""
        pass

    @abstractmethod
    def save_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """Saves a pandas DataFrame to the specified table in the database"""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns the result as a pandas DataFrame"""
        pass
