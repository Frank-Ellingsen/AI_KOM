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

    # 7. PDF Reports
    p_pdf = subparsers.add_parser("pdf-report", help="Generer månedlige PDF- og lederrapporter for budsjettansvarlige")
    p_pdf.add_argument("--month", type=int, default=9, help="Månedsnummer (1..12)")
    p_pdf.add_argument("--ansvar-id", type=str, default=None, help="Filtrer på spesifikk ansvar_id")
    p_pdf.add_argument("--all", action="store_true", help="Generer for alle enheter")

    # 8. Rapportarkiv for hver budsjettansvarlig
    p_arkiv = subparsers.add_parser("arkiv", help="Bygg individuelle rapportarkiver for alle 41 budsjettansvarlige")
    p_arkiv.add_argument("--unit", type=str, default=None, help="Filtrer på spesifikk ansvar_id")

    # 9. M10 Month-End Ingestion
    p_m10 = subparsers.add_parser("m10-ingest", help="M10 Oktober staging og manuell push-button innlesing")
    p_m10.add_argument("--status", action="store_true", help="Vis staging-kø status")
    p_m10.add_argument("--execute", action="store_true", help="Utfør manuell innlesing med SHA-256 stempel")
    p_m10.add_argument("--approved-by", default="frank.ellingsen@kristiansand.kommune.no", help="Godkjennende saksbehandler")
    p_m10.add_argument("--role", default="Senior_Controller", help="Rolle for godkjenner")
    p_m10.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 10. MVA Balansekonto 2130 Validering
    p_mva = subparsers.add_parser("mva", help="Kvalitetskontroll og avstemming mot Balansekonto 2130 (MVA)")
    p_mva.add_argument("--file", default="data/repostings/Ompostering_Korreksjonsfil_ERP_Eksport_v2.xlsx", help="Sti til korreksjonsfil (.xlsx)")
    p_mva.add_argument("--report", default="reports/test_mva_balanse_2130_rapport.md", help="Sti til utgående rapport (.md)")
    p_mva.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 11. Fast-Path Triage Router
    p_triage = subparsers.add_parser("triage", help="Fast-Path Triage Router for forespørselsklassifisering")
    p_triage.add_argument("prompt", nargs="?", default="Hva sier Kommuneloven § 14-5 om overskridelse av årsbudsjett?", help="Brukerhenvendelse")
    p_triage.add_argument("--persona", default="CONTROLLER", help="Aktiv persona (CONTROLLER, ENHETSLEDER)")
    p_triage.add_argument("--unit", default="2020", help="Aktiv enhets-ID")
    p_triage.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 12. Cash Management & Likviditetsstyring
    p_cash = subparsers.add_parser("cash", help="Cash Management & Likviditetsstyring (M11 rullende prognose, kassakreditt og What-If simulering)")
    p_cash.add_argument("--position", action="store_true", help="Vis konsernkonto og kassakredittstatus")
    p_cash.add_argument("--forecast", action="store_true", help="Vis 30-dagers rullende likviditetsprognose")
    p_cash.add_argument("--simulate", action="store_true", help="Kjør What-If scenariesimulering")
    p_cash.add_argument("--compliance", action="store_true", help="Valider mot Kommuneloven § 14-14 og Finansforskriften")
    p_cash.add_argument("--scenario-name", default="Simulert Avvik", help="Navn på scenario")
    p_cash.add_argument("--tax-delta", type=float, default=-5.0, help="Endring i skatt (prosent)")
    p_cash.add_argument("--grant-delay", type=int, default=5, help="Forsinkelse på rammetilskudd (dager)")
    p_cash.add_argument("--extra-expense", type=float, default=2500000.0, help="Ekstraordinær kostnad (NOK)")
    p_cash.add_argument("--credit-limit", type=float, default=150000000.0, help="Kassakredittramme (NOK)")
    p_cash.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 13. Top 3 KPIs & Budsjetthierarki
    p_kpi = subparsers.add_parser("kpi", help="Top 3 Kommunale Nøkkeltall (Takometer/Gauge) og kaskaderende budsjetthierarki")
    p_kpi.add_argument("--sector", type=str, default=None, help="Filtrer på spesifikk sektor (f.eks. OMR-02)")
    p_kpi.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 14. Bystyret PowerPoint Export (.pptx)
    p_pptx = subparsers.add_parser("pptx", help="Automatisert Bystyre og Formannskap PowerPoint eksport (.pptx)")
    p_pptx.add_argument("--out", type=str, default="reports/Bystyret_M10_Okonomi_Rapport.pptx", help="Utfilsti (.pptx)")
    p_pptx.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 15. Agent 13: Evaluation & QA Agent
    p_eval = subparsers.add_parser("eval", help="Agent 13: Evaluation & QA Runner (Golden Dataset, RAG-evaluering, 90 %% CI/CD Gate)")
    p_eval.add_argument("--golden", action="store_true", help="Kjør evaluering mot Golden Dataset")
    p_eval.add_argument("--gate", action="store_true", help="Valider og håndhev 90 %% CI/CD kvalitetsport")
    p_eval.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 16. Agent 14: Database & Data Engineering Agent
    p_db = subparsers.add_parser("db", help="Agent 14: Database & Data Engineering Runner (Schema, Read-Only SQL, EXPLAIN, Hybridsøk)")
    p_db.add_argument("--inspect-schema", nargs="?", const="ALL", default=None, help="Inspiser tabellskjema og indekser")
    p_db.add_argument("--query", type=str, help="Kjør parametrisert SQL-spørring")
    p_db.add_argument("--explain", type=str, help="Kjør EXPLAIN QUERY PLAN og gi optimaliseringsråd")
    p_db.add_argument("--hybrid-search", type=str, help="Kjør hybridsøk (Sparse FTS5 + Dense Vektor)")
    p_db.add_argument("--hitl", action="store_true", help="Bekreft Human-in-the-Loop for skriveoperasjon")
    p_db.add_argument("--limit", type=int, default=50, help="Maks rader (standard: 50)")
    p_db.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 17. Agent 15: AI Engineering & Infrastructure Agent
    p_aie = subparsers.add_parser("ai-eng", help="Agent 15: AI Engineering & Infrastructure Runner (4-lags arkitektur, caching, benchmarking)")
    p_aie.add_argument("--status", action="store_true", help="Vis helsestatus for de 4 arkitekturlagene")
    p_aie.add_argument("--compact", type=str, help="Kjør kontekstkomprimering og bevar lovhenvisninger")
    p_aie.add_argument("--benchmark", action="store_true", help="Mål inferenslatens, TTFT og tokengjennomstrømming")
    p_aie.add_argument("--cache-stats", action="store_true", help="Vis statistikk og besparelser for semantisk cache")
    p_aie.add_argument("--json", action="store_true", help="Formatér respons som JSON")

    # 18. Advisor Knowledge Ingestion
    p_adv = subparsers.add_parser("advisor-ingest", help="Ingest og oppdater kunnskapsmoduler for kommunale økonomirådgivere")

    # 19. Advisor Decision Calculators
    p_calc = subparsers.add_parser("advisor-calc", help="Beslutnings- og Beregningsmotor for Økonomirådgivere (NAV-gap, KRS 4, Selvkost, MVA)")
    p_calc.add_argument("--type", choices=["nav-gap", "krs4", "selvkost", "mva-10y"], required=True, help="Beregningstype")

    # 20. Municipal Advisor Full-Year Stress Test
    p_stress = subparsers.add_parser("advisor-stress", help="Full-Year Stresstest & Flaskehalsdiagnose for Kommunale Rådgivere (M1-M12, 6 Sektorer)")

    # 21. DuckDB OLAP Engine
    p_duck = subparsers.add_parser("duckdb", help="Kjør in-memory DuckDB OLAP-aggregasjon, EVM-prognose og kostnadsdrivere")
    p_duck.add_argument("--summary", action="store_true", help="Vis samlet EVM-oppsummering for alle 6 virksomhetsområder")
    p_duck.add_argument("--sector", type=str, default=None, help="Filtrer på spesifikt virksomhetsområde")
    p_duck.add_argument("--unit", type=str, default=None, help="Vis enhetsdrilldown")
    p_duck.add_argument("--drivers", action="store_true", help="Vis topp 10 kostnadsdrivere (Art)")
    p_duck.add_argument("--query", type=str, default=None, help="Kjør vilkårlig DuckDB SQL-spørring")
    p_duck.add_argument("--year", type=int, default=2026, help="Regnskapsår (standard: 2026)")
    p_duck.add_argument("--month", type=int, default=9, help="Måned YTD (standard: 9)")
    p_duck.add_argument("--json", action="store_true", help="Formatér respons som JSON")

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
    elif args.command == "pdf-report":
        cmd_args = ["--month", str(args.month)]
        if args.ansvar_id:
            cmd_args += ["--ansvar-id", args.ansvar_id]
        if args.all:
            cmd_args.append("--all")
        run_command("generate_monthly_pdf_reports.py", cmd_args + unknown)
    elif args.command == "arkiv":
        cmd_args = []
        if args.unit:
            cmd_args += ["--unit", args.unit]
        run_command("build_budsjettansvarlige_arkiver.py", cmd_args + unknown)
    elif args.command == "m10-ingest":
        cmd_args = []
        if args.execute:
            cmd_args.append("--execute")
        if args.status:
            cmd_args.append("--status")
        if args.approved_by:
            cmd_args += ["--approved-by", args.approved_by]
        if args.role:
            cmd_args += ["--role", args.role]
        if args.json:
            cmd_args.append("--json")
        run_command("m10_ingestion_runner.py", cmd_args + unknown)
    elif args.command == "mva":
        cmd_args = ["--export-file", args.file, "--report-out", args.report]
        if args.json:
            cmd_args.append("--json")
        run_command("mva_balanse_validator.py", cmd_args + unknown)
    elif args.command == "triage":
        cmd_args = [args.prompt, "--persona", args.persona, "--unit", args.unit]
        if args.json:
            cmd_args.append("--json")
        run_command("triage_cli.py", cmd_args + unknown)
    elif args.command == "cash":
        cmd_args = []
        if args.position:
            cmd_args.append("--position")
        if args.forecast:
            cmd_args.append("--forecast")
        if args.simulate:
            cmd_args.append("--simulate")
        if args.compliance:
            cmd_args.append("--compliance")
        if args.scenario_name:
            cmd_args += ["--scenario-name", args.scenario_name]
        if args.tax_delta != -5.0:
            cmd_args += ["--tax-delta", str(args.tax_delta)]
        if args.grant_delay != 5:
            cmd_args += ["--grant-delay", str(args.grant_delay)]
        if args.extra_expense != 2500000.0:
            cmd_args += ["--extra-expense", str(args.extra_expense)]
        if args.credit_limit != 150000000.0:
            cmd_args += ["--credit-limit", str(args.credit_limit)]
        if args.json:
            cmd_args.append("--json")
        run_command("cash_management_runner.py", cmd_args + unknown)
    elif args.command == "kpi":
        cmd_args = []
        if args.sector:
            cmd_args += ["--sector", args.sector]
        if args.json:
            cmd_args.append("--json")
        run_command("kpi_runner.py", cmd_args + unknown)
    elif args.command == "pptx":
        cmd_args = ["--out", args.out]
        if args.json:
            cmd_args.append("--json")
        run_command("report_export_runner.py", cmd_args + unknown)
    elif args.command == "eval":
        cmd_args = []
        if args.golden:
            cmd_args.append("--golden")
        if args.gate:
            cmd_args.append("--gate")
        if args.json:
            cmd_args.append("--json")
        run_command("evaluation_runner.py", cmd_args + unknown)
    elif args.command == "db":
        cmd_args = []
        if args.inspect_schema:
            cmd_args += ["--inspect-schema", args.inspect_schema]
        if args.query:
            cmd_args += ["--query", args.query]
        if args.explain:
            cmd_args += ["--explain", args.explain]
        if args.hybrid_search:
            cmd_args += ["--hybrid-search", args.hybrid_search]
        if args.hitl:
            cmd_args.append("--hitl")
        if args.limit != 50:
            cmd_args += ["--limit", str(args.limit)]
        if args.json:
            cmd_args.append("--json")
        run_command("database_runner.py", cmd_args + unknown)
    elif args.command == "ai-eng":
        cmd_args = []
        if args.status:
            cmd_args.append("--status")
        if args.compact:
            cmd_args += ["--compact", args.compact]
        if args.benchmark:
            cmd_args.append("--benchmark")
        if args.cache_stats:
            cmd_args.append("--cache-stats")
        if args.json:
            cmd_args.append("--json")
        run_command("ai_engineering_runner.py", cmd_args + unknown)
    elif args.command == "advisor-ingest":
        run_command("ingest_municipal_advisor_knowledge.py", unknown)
    elif args.command == "advisor-calc":
        run_command("advisor_calculator_runner.py", ["--type", args.type] + unknown)
    elif args.command == "advisor-stress":
        run_command("advisor_stresstest_engine.py", unknown)
    elif args.command == "duckdb":
        cmd_args = []
        if args.summary:
            cmd_args.append("--summary")
        if args.sector:
            cmd_args += ["--sector", args.sector]
        if args.unit:
            cmd_args += ["--unit", args.unit]
        if args.drivers:
            cmd_args.append("--drivers")
        if args.query:
            cmd_args += ["--query", args.query]
        if args.year != 2026:
            cmd_args += ["--year", str(args.year)]
        if args.month != 9:
            cmd_args += ["--month", str(args.month)]
        if args.json:
            cmd_args.append("--json")
        run_command("duckdb_runner.py", cmd_args + unknown)

if __name__ == "__main__":
    main()
