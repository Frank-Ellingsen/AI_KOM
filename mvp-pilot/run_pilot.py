#!/usr/bin/env python3
"""
MVP Pilot Runner - Kristiansand Kommune AI Kommunal Økonomistyring
CLI Entry Point for the entire workflow.
"""

import argparse
import sys
import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_etl():
    print("\n[STEG 1/4] Kjører ETL Ingestion...")
    from etl import ingest_excel_to_databases
    return ingest_excel_to_databases()

def run_forecast():
    print("\n[STEG 2/4] Kjører Prediktiv EAC/ETC Modellering...")
    from eac_forecasting import compute_eac_forecasts
    f = compute_eac_forecasts()
    print(f"      • EAC (AI Sesongmodell): {f['models']['driver_based_ai']['eac']:,.2f} kr")
    print(f"      • Avvik mot årsbudsjett:  {f['models']['driver_based_ai']['variance']:,.2f} kr")
    return f

def run_prescriptive():
    print("\n[STEG 3/4] Kjører Preskriptiv AI Tiltaksagent (Ollama)...")
    from prescriptive_agent import evaluate_measures_with_ai
    res = evaluate_measures_with_ai()
    print(f"      • AI Vurdering: {res['llm_commentary']}")
    return res

def run_report():
    print("\n[STEG 4/4] Genererer Edward Tufte Økonominotat...")
    from executive_report import generate_executive_memo
    p = generate_executive_memo()
    print(f"      • Notat lagret: {p}")
    return p

def run_ui():
    print("\n[UI] Starter Streamlit HITL Portalen...")
    streamlit_exe = shutil.which("streamlit")
    if not streamlit_exe:
        print("[FEIL] 'streamlit' ikke funnet. Kjør: pip install streamlit")
        sys.exit(1)
    subprocess.run([streamlit_exe, "run", str(ROOT / "app_ui.py")], cwd=str(ROOT))

def main():
    parser = argparse.ArgumentParser(description="MVP-Pilot: AI i kommunal økonomistyring (Bo og Miljø)")
    parser.add_argument("--etl", action="store_true", help="Kjør data ingestion fra Excel til DuckDB/SQLite")
    parser.add_argument("--forecast", action="store_true", help="Beregn EAC/ETC prognoser")
    parser.add_argument("--agent", action="store_true", help="Kjør preskriptiv AI-tiltaksagent")
    parser.add_argument("--report", action="store_true", help="Generer Tufte økonominotat")
    parser.add_argument("--pipeline", action="store_true", help="Kjør hele analyse- og rapportpipelinen")
    parser.add_argument("--ui", action="store_true", help="Start Streamlit web-grensesnittet")

    args = parser.parse_args()

    # Hvis ingen argumenter, kjør pipeline som standard
    if not any([args.etl, args.forecast, args.agent, args.report, args.pipeline, args.ui]):
        args.pipeline = True

    if args.etl or args.pipeline:
        run_etl()
    if args.forecast or args.pipeline:
        run_forecast()
    if args.agent or args.pipeline:
        run_prescriptive()
    if args.report or args.pipeline:
        run_report()
    if args.ui:
        run_ui()

    print("\n[OK] Pilotkjøring fullført!")

if __name__ == "__main__":
    main()
