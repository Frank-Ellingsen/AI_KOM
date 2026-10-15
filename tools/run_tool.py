#!/usr/bin/env python3
"""
Kristiansand Kommune — Unified CLI Tool Runner
Sentral kommandolinje for alle lokale AI-verktøy, prognosemotorer og revisjonsvalideringer.
"""

import sys
import os
import argparse
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_command(script_name, args):
    tool_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(tool_path):
        print(f"Feil: Verktøyet '{script_name}' ble ikke funnet i tools/ ({tool_path})")
        sys.exit(1)
    
    cmd = [sys.executable, tool_path] + args
    print(f"[*] Kjører: {' '.join(cmd)}\n" + "-" * 60)
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Kristiansand Kommune — Unified AI Controller Tool Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Eksempler på bruk:
  python tools/run_tool.py forecast --mode both
  python tools/run_tool.py audit
  python tools/run_tool.py excel
  python tools/run_tool.py verify
  python tools/run_tool.py server --port 8000
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Tilgjengelige verktøy")

    # 1. Forecast
    p_forecast = subparsers.add_parser("forecast", help="Kjør prediktiv AI-prognose (Monte Carlo P10/P50/P90 & EVM)")
    p_forecast.add_argument("--mode", choices=["drift", "investering", "both"], default="both", help="Prognosemodus")
    p_forecast.add_argument("--db", default="erp_data/kommune_golden_record.db", help="Sti til SQLite-database")

    # 2. Audit
    p_audit = subparsers.add_parser("audit", help="Kjør internkontroll og revisjonsvalidering jf. Kommuneloven § 14-5")
    p_audit.add_argument("--db", default="erp_data/kommune_golden_record.db", help="Sti til SQLite-database")

    # 3. Excel
    p_excel = subparsers.add_parser("excel", help="Generer offisiell Excel Controller-rapport (FAST Standard)")
    p_excel.add_argument("--out", default="reports/Kommune_Project_Controller_Reporting_2026.xlsx", help="Utfilsti")

    # 4. Verify
    p_verify = subparsers.add_parser("verify", help="Verifiser helsetilstand for Control Office Hub")

    # 5. Server
    p_server = subparsers.add_parser("server", help="Start lokal Hub API server")
    p_server.add_argument("--port", type=int, default=8000, help="Portnummer")

    # 6. Parse
    p_parse = subparsers.add_parser("parse", help="Parse dokument (PDF/Word/Excel) til tekst")
    p_parse.add_argument("file", help="Sti til fil som skal parses")

    args, unknown = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "forecast":
        run_command("predictive_forecasting_engine.py", ["--mode", args.mode, "--db", args.db] + unknown)
    elif args.command == "audit":
        run_command("audit_revisjon_validator.py", ["--db", args.db] + unknown)
    elif args.command == "excel":
        run_command("generate_controller_excel_report.py", unknown)
    elif args.command == "verify":
        run_command("verify_office_hub.py", unknown)
    elif args.command == "server":
        run_command("hub_api_server.py", ["--port", str(args.port)] + unknown)
    elif args.command == "parse":
        run_command("document_parser.py", [args.file] + unknown)

if __name__ == "__main__":
    main()
