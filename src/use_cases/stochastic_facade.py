import json
import os
from pathlib import Path
from pyspark.sql import SparkSession
from src.core.models.markov_model import MarkovModel
from src.core.models.queuing_model import QueuingModel
from src.core.security.audit_logger import AuditLogger

class StochasticFacade:
    def __init__(self):
        self.logger = AuditLogger()
        self.markov = MarkovModel()
        self.queuing = QueuingModel()
        self.results_dir = Path("docs/MODELS_RESULTS")
        
    def run_all(self):
        self.logger.info("StochasticFacade", "Starting stochastic model execution...")
        
        try:
            spark = SparkSession.builder.getOrCreate()
            gold_path = "data/gold/Aggr_NPS"
            
            if not os.path.exists(gold_path):
                self.logger.error("StochasticFacade", "Gold layer not found.")
                return False
                
            df = spark.read.format("delta").load(gold_path).toPandas()
            
            final_results = {}
            
            # Global
            final_results["Todos los Bancos"] = {
                "markov_chains": self.markov.calculate(df),
                "queuing_theory": self.queuing.calculate(df)
            }
            
            # Por Banco
            if "bank_name" in df.columns:
                for bank in df["bank_name"].unique():
                    df_bank = df[df["bank_name"] == bank]
                    final_results[bank] = {
                        "markov_chains": self.markov.calculate(df_bank),
                        "queuing_theory": self.queuing.calculate(df_bank)
                    }
            
            self.results_dir.mkdir(parents=True, exist_ok=True)
            with open(self.results_dir / "stochastic_results.json", "w") as f:
                json.dump(final_results, f, indent=4)
                
            self.logger.info("StochasticFacade", "Results saved to stochastic_results.json successfully.")
            return True
            
        except Exception as e:
            self.logger.error("StochasticFacade", f"Pipeline failed: {str(e)}")
            return False
