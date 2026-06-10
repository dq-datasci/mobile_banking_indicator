import duckdb
import pandas as pd
import threading
from pathlib import Path
from src.core.interfaces.database_interface import IDatabase

class DuckDBConnection(IDatabase):
    """
    DuckDB implementation of the IDatabase interface using the Singleton pattern.
    Ensures that only one connection to the database is maintained throughout
    the application lifecycle, reducing memory overhead.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str = "data/database.duckdb"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DuckDBConnection, cls).__new__(cls)
                cls._instance._db_path = db_path
                cls._instance._conn = None
        return cls._instance

    def connect(self) -> None:
        """Establishes connection to the database using DuckDB."""
        if self._conn is None:
            # Ensure the directory exists
            Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = duckdb.connect(self._db_path)
            
    def save_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Saves a pandas DataFrame to the specified table in DuckDB.
        Appends the data to the existing table or creates it if it doesn't exist.
        """
        if self._conn is None:
            self.connect()
        # Register dataframe as a virtual table in DuckDB
        self._conn.register('temp_df', df)
        # Create table if it does not exist based on the structure of the dataframe
        self._conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM temp_df WHERE 1=0")
        # Insert data
        self._conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df")
        # Unregister virtual table
        self._conn.unregister('temp_df')

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns the result as a pandas DataFrame."""
        if self._conn is None:
            self.connect()
        return self._conn.execute(query).fetchdf()

    def get_connection(self):
        """Returns the raw duckdb connection object if needed."""
        if self._conn is None:
            self.connect()
        return self._conn
