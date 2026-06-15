from src.use_cases.stochastic_facade import StochasticFacade
from pyspark.sql import SparkSession

def main():
    print("Iniciando Pipeline de Modelos Estocásticos (Cadenas de Markov y Teoría de Colas)...")
    
    spark = SparkSession.builder \
        .appName("OmniVoC-Stochastic") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[*]") \
        .getOrCreate()
        
    facade = StochasticFacade()
    success = facade.run_all()
    
    if success:
        print("Pipeline estocástico finalizado exitosamente. Revisa docs/MODELS_RESULTS/stochastic_results.json")
    else:
        print("Error en el pipeline estocástico.")

if __name__ == "__main__":
    main()
