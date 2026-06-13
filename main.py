import argparse
import sys
import subprocess
from pathlib import Path

def run_silver():
    print("Iniciando Pipeline Silver...")
    subprocess.run(["python", "-m", "src.infrastructure.pipelines.silver_pipeline"], check=True)

def run_gold():
    print("Iniciando Pipeline Gold...")
    subprocess.run(["python", "-m", "src.infrastructure.pipelines.gold_pipeline"], check=True)

def run_models():
    print("Iniciando Modelos Econométricos (Logit y NPS)...")
    subprocess.run(["python", "-m", "src.core.models.nps_calculator"], check=True)
    subprocess.run(["python", "-m", "src.core.models.churn_logit"], check=True)

def run_stochastic():
    print("Iniciando Modelos Estocásticos (Markov y Colas)...")
    subprocess.run(["python", "-m", "src.core.models.train_stochastic"], check=True)

def run_automl():
    print("Iniciando PyCaret AutoML Baseline...")
    subprocess.run(["python", "-m", "src.core.models.train_automl"], check=True)

def run_dashboard():
    print("Iniciando Dashboard Interactivo en el puerto 8501...")
    subprocess.run(["streamlit", "run", "src/presentation/dashboard.py"])

def main():
    parser = argparse.ArgumentParser(description="OmniVoC CLI Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    subparsers.add_parser("run-silver", help="Ejecuta la limpieza y procesamiento en Silver Layer (PySpark)")
    subparsers.add_parser("run-gold", help="Ejecuta el Feature Engineering y Star Schema en Gold Layer (PySpark)")
    subparsers.add_parser("run-models", help="Calcula el modelo Logit de Churn y el NPS")
    subparsers.add_parser("run-automl", help="Ejecuta el entrenamiento de modelos base con PyCaret MLflow")
    subparsers.add_parser("run-dashboard", help="Despliega el Dashboard Interactivo localmente (Streamlit)")
    subparsers.add_parser("run-stochastic", help="Ejecuta los modelos estocásticos (Markov y Colas)")
    subparsers.add_parser("run-all", help="Ejecuta todo el pipeline End-to-End (desde Silver hasta Modelos)")

    args = parser.parse_args()

    if args.command == "run-silver":
        run_silver()
    elif args.command == "run-gold":
        run_gold()
    elif args.command == "run-models":
        run_models()
    elif args.command == "run-automl":
        run_automl()
    elif args.command == "run-stochastic":
        run_stochastic()
    elif args.command == "run-dashboard":
        run_dashboard()
    elif args.command == "run-all":
        run_silver()
        run_gold()
        run_models()
        run_stochastic()
        run_automl()
        print("Pipeline backend finalizado. Usa 'run-dashboard' para visualizar.")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
