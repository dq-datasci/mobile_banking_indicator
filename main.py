import argparse
import sys
import subprocess
from pathlib import Path

def run_silver():
    print("Iniciando Pipeline Silver...")
    subprocess.run(["python", "src/infrastructure/pipelines/silver_pipeline.py"], check=True)

def run_gold():
    print("Iniciando Pipeline Gold...")
    subprocess.run(["python", "src/infrastructure/pipelines/gold_pipeline.py"], check=True)

def run_models():
    print("Iniciando Modelos Econométricos (Logit y NPS)...")
    subprocess.run(["python", "src/core/models/nps_calculator.py"], check=True)
    subprocess.run(["python", "src/core/models/churn_logit.py"], check=True)

def run_dashboard():
    print("Iniciando Dashboard Interactivo en el puerto 8501...")
    subprocess.run(["streamlit", "run", "src/presentation/dashboard.py"])

def main():
    parser = argparse.ArgumentParser(description="OmniVoC CLI Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    subparsers.add_parser("run-silver", help="Ejecuta la limpieza y procesamiento en Silver Layer (PySpark)")
    subparsers.add_parser("run-gold", help="Ejecuta el Feature Engineering y Star Schema en Gold Layer (PySpark)")
    subparsers.add_parser("run-models", help="Calcula el modelo Logit de Churn y el NPS")
    subparsers.add_parser("run-dashboard", help="Despliega el Dashboard Interactivo localmente (Streamlit)")
    subparsers.add_parser("run-all", help="Ejecuta todo el pipeline End-to-End (desde Silver hasta Modelos)")

    args = parser.parse_args()

    if args.command == "run-silver":
        run_silver()
    elif args.command == "run-gold":
        run_gold()
    elif args.command == "run-models":
        run_models()
    elif args.command == "run-dashboard":
        run_dashboard()
    elif args.command == "run-all":
        run_silver()
        run_gold()
        run_models()
        print("Pipeline backend finalizado. Usa 'run-dashboard' para visualizar.")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
