"""
Master Test Suite for Kristiansand Kommune AI Guardrails & Control Office Hub
Tester alle kjernedimensjoner i prosjektet:
1. Hub V2 UI & filstruktur (86/86 sjekker)
2. Kommunerevisjonen & Kontrollutvalget revisjonstester (SHA-256, HITL, PII)
3. Prediktiv AI & EVM controllingberegninger
4. MVP Pilot datagrunnlag og avstemming (DuckDB/SQLite)
5. MCP Server & Glass-Box RAG spørringer
"""
import os
import sys
from pathlib import Path
import pytest
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
GUARDRAILS_DIR = ROOT_DIR / "kommune-ai-guardrails"
SRC_DIR = GUARDRAILS_DIR / "src"
ERP_DIR = ROOT_DIR / "erp_data"
TOOLS_DIR = ROOT_DIR / "tools"
MVP_DIR = ROOT_DIR / "mvp-pilot"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
if str(MVP_DIR) not in sys.path:
    sys.path.insert(0, str(MVP_DIR))


def test_office_hub_v2_and_templates_verification():
    """Validerer at Office Hub V2, maler, lenker og spesifikasjoner er 100 % intakte."""
    from verify_office_hub import (
        EXPECTED_MOVED_FILES,
        EXPECTED_DOCX_FILES,
        StrictHTMLValidator
    )
    import re

    # 1. Rot-mappen skal være ryddet for ad-hoc dokumenter (kun godkjente rot-md-filer tillatt)
    ALLOWED_ROOT_MDS = {"README.md", "AGENTS.md", "INDEX.md"}
    root_mds = [f.name for f in ROOT_DIR.glob("*.md")]
    unexpected_root_mds = set(root_mds) - ALLOWED_ROOT_MDS
    assert not unexpected_root_mds, f"Uventede md-filer i rot: {unexpected_root_mds}"

    # 2. Alle flyttede md-filer skal eksistere og ha innhold
    for f in EXPECTED_MOVED_FILES:
        assert f.exists() and f.stat().st_size > 100, f"Mangler: {f}"

    # 3. Word-maler skal eksistere
    for f in EXPECTED_DOCX_FILES:
        assert f.exists() and f.stat().st_size > 1000, f"Mangler docx: {f}"

    # 4. index.html skal være velformet
    index_file = ROOT_DIR / "index.html"
    assert index_file.exists(), "index.html finnes ikke"
    html_content = index_file.read_text(encoding="utf-8")
    parser = StrictHTMLValidator()
    parser.feed(html_content)
    assert len(parser.errors) == 0, f"HTML parser feil: {parser.errors}"

    # 5. Alle dokumentlenker i index.html skal peke til eksisterende filer
    file_hrefs = re.findall(r'href=[\"\'](templates/.*?|reports/.*?|docs/.*?|bruker-guides/.*?|generic-ai-pilot-pakke/.*?|antigravity-ms-pilot/.*?)[\"\']', html_content)
    for href in set(file_hrefs):
        assert (ROOT_DIR / href).exists(), f"Brutt lenke: {href}"


def test_audit_revisjon_compliance():
    """Validerer Kommunerevisjonens kontrollpunkter (Port 4, 8, 9, 10)."""
    db_path = ERP_DIR / "kommune_golden_record.db"
    assert db_path.exists(), "Fant ikke kommune_golden_record.db"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. SHA-256 integritet
    cur.execute("SELECT sha256_hash FROM Fact_Prognose_Logg")
    prog_rows = cur.fetchall()
    assert len(prog_rows) > 0, "Ingen prognoser i Fact_Prognose_Logg"
    for (h,) in prog_rows:
        assert len(h) == 64, f"Ugyldig SHA-256 lengde: {h}"

    # 2. Human-in-the-Loop navngitt saksbehandler
    cur.execute("SELECT saksbehandler FROM Fact_Prognose_Logg")
    saksb_rows = cur.fetchall()
    for (s,) in saksb_rows:
        assert s is not None and len(s) > 0, "Mangler saksbehandler"
        assert "Frank" in s or "Ellingsen" in s, f"Uautorisert saksbehandler: {s}"

    # 3. PII-skjerming
    cur.execute("SELECT count(*) FROM stg_erp_transactions WHERE description LIKE '%fnr%' OR description LIKE '%12058%'")
    pii_count = cur.fetchone()[0]
    assert pii_count == 0, "PII funnet i stg_erp_transactions"

    # 4. § 14-5 terskelvarsling
    cur.execute("SELECT count(*) FROM Fact_Prognose_Logg WHERE status = 'KRITISK_MERFORBRUK'")
    crit_count = cur.fetchone()[0]
    assert crit_count >= 2, f"Forventet minst 2 kritiske enheter, fant {crit_count}"

    conn.close()


def test_predictive_forecasting_engine_calculations():
    """Tester Monte Carlo sjåførberegninger og EVM kostnadskontroll."""
    from predictive_forecasting_engine import calculate_operational_forecast, calculate_project_evm_forecast

    # Test driftsmodell
    drift = calculate_operational_forecast(
        hittil_regnskap_ac=47426244.0,
        gjeldende_maned=8,
        vedtatt_ramme_bac=50339572.0,
        n_simuleringer=5000
    )
    assert drift["p10_optimistisk"] < drift["p50_forventet"] < drift["p90_konservativt"]
    assert drift["status"] == "KRITISK_MERFORBRUK"
    assert len(drift["sha256_hash"]) == 64

    # Test EVM investeringsmodell
    evm = calculate_project_evm_forecast(
        bac=200000000.0,
        pv=120000000.0,
        ev=110000000.0,
        ac=125000000.0,
        usikkerhet_p85_tillegg=0.08
    )
    assert evm["cpi"] < 1.0  # AC > EV betyr CPI < 1
    assert evm["spi"] < 1.0  # EV < PV betyr SPI < 1
    assert evm["eac_p50"] > 200000000.0
    assert len(evm["sha256_hash"]) == 64


def test_mvp_pilot_data_and_eac():
    """Tester MVP-pilotens beregninger og balanser for Bo og Miljø."""
    from eac_forecasting import compute_eac_forecasts
    forecasts = compute_eac_forecasts()
    assert "models" in forecasts
    assert "driver_based_ai" in forecasts["models"]
    eac = forecasts["models"]["driver_based_ai"]["eac"]
    assert eac > 17000000.0, f"Uventet lav EAC: {eac}"


def test_mcp_server_law_search_and_financials():
    """Tester MCP-verktøy for lovoppslag og økonomitall."""
    from kommune_ai_guardrails.mcp_server import search_municipal_law, get_unit_financials

    # Lovoppslag
    laws = search_municipal_law("Kommuneloven § 14-5", top_k=2)
    assert len(laws) > 0
    assert any("14-5" in l["paragraf"] for l in laws)

    # Økonomitall
    fin = get_unit_financials(unit_id="202", period="Q2")
    assert fin["unit_id"] == "202"
    assert fin["actual_ytd"] > 0
    assert fin["variance_nok"] < 0  # Avvik = Budsjett - Faktisk (negativt ved merforbruk)


def test_hub_api_server_endpoints():
    """Tester lokale API-endepunkter i hub_api_server."""
    from hub_api_server import handle_rag_query, get_financial_summary

    # RAG endpoint
    rag_res = handle_rag_query("Hva krever § 14-5?", top_k=2)
    assert rag_res["ok"] is True
    assert len(rag_res["sha256"]) == 64
    assert rag_res["results_count"] > 0

    # Financial summary
    fin_summary = get_financial_summary()
    assert fin_summary["ok"] is True
    assert fin_summary["actual_ytd_nok"] > 0
    assert fin_summary["budget_ytd_nok"] > 0


def test_antigravity_ms_pilot_and_generic_package_compliance():
    """Validerer at antigravity-ms-pilot og generic-ai-pilot-pakke er intakte og funksjonelle."""
    import json

    # 1. Sjekk generic-ai-pilot-pakke
    gen_root = ROOT_DIR / "generic-ai-pilot-pakke"
    assert (gen_root / "README.md").exists(), "Mangler generic-ai-pilot-pakke/README.md"
    assert (gen_root / "enterprise-ai-pilot" / "README.md").exists(), "Mangler enterprise-ai-pilot/README.md"
    assert (gen_root / "enterprise-ai-pilot" / "dax_and_analytics" / "01_generisk_dax_og_rag_formatering.dax").exists()

    # 2. Sjekk antigravity-ms-pilot subprosjektstruktur
    sub_root = ROOT_DIR / "antigravity-ms-pilot"
    assert (sub_root / "README.md").exists()
    assert (sub_root / "pyproject.toml").exists()
    assert (sub_root / "requirements.txt").exists()
    assert (sub_root / "run_pilot.py").exists()

    # 3. Test subprosjekt kildekode import
    sub_src = sub_root / "src"
    if str(sub_src) not in sys.path:
        sys.path.insert(0, str(sub_src))

    from gateway.pii_scrubber import sanitize_pii
    from utils.audit_logger import AuditLogger

    # Test PII vask
    clean = sanitize_pii("Enhet 202 saksbehandler FNR 12058512345 tlf 98765432")
    assert "12058512345" not in clean
    assert "98765432" not in clean
    assert "[SKJERMET_FNR]" in clean

    # Test SHA-256 forsegling
    logger = AuditLogger()
    entry = logger.log_action("Test query", "Test response", actor="Frank Ellingsen")
    assert len(entry.sha256_hash) == 64
    assert entry.actor == "Frank Ellingsen"

    # 4. Sjekk Ground Truth eval data
    eval_file = sub_root / "evals" / "01_ground_truth_eval_template.json"
    assert eval_file.exists()
    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    assert eval_data["target_faithfulness"] == 1.00


def test_antigravity_backend_and_mlops_packages_integration():
    """Validerer at antigravity_backend_module_pakke og AI_KOM_MLOps_og_Navigasjon_pakke er integrert og testet."""
    # 1. Sjekk antigravity_backend_module_pakke
    backend_pkg = ROOT_DIR / "antigravity_backend_module_pakke"
    assert (backend_pkg / "ANTIGRAVITY_backend_architecture.md").exists()
    assert (backend_pkg / "ANTIGRAVITY_data_pipeline_and_connectors.md").exists()
    assert (backend_pkg / "ANTIGRAVITY_ai_rag_services.md").exists()
    assert (backend_pkg / "ANTIGRAVITY_api_spec_and_deployment.md").exists()

    # 2. Sjekk AI_KOM_MLOps_og_Navigasjon_pakke
    mlops_pkg = ROOT_DIR / "AI_KOM_MLOps_og_Navigasjon_pakke"
    assert (mlops_pkg / "AI_KOM_layout_og_navigasjon-v2.md").exists()
    assert (mlops_pkg / "AI_KOM_MLOps_og_Data_Lineage.md").exists()
    assert (mlops_pkg / "README.md").exists()

    # 3. Test at hub_api_server har v1 OpenAPI-tjenester operative
    from hub_api_server import (
        get_v1_finance_overview,
        get_v1_unit_m9,
        verify_v1_audit_hash,
        get_v1_port9_logs,
        sign_v1_port9
    )

    overview = get_v1_finance_overview()
    assert overview["ok"] is True
    assert overview["total_aarsbudsjett_nok"] == 7240000000.0

    unit = get_v1_unit_m9("2020")
    assert unit["ok"] is True
    assert unit["unit_id"] == "2020"

    sign = sign_v1_port9({"unit_id": "2020", "decision": "APPROVED", "notes": "Integrasjonstest"})
    assert sign["ok"] is True
    assert len(sign["document_sha256"]) == 64

    verify = verify_v1_audit_hash(sign["document_sha256"])
    assert verify["ok"] is True
    assert verify["verified"] is True

    logs = get_v1_port9_logs()
    assert logs["ok"] is True
    assert logs["count"] >= 0

    # 4. Sjekk at index.html har seksjon 3.4
    index_html = (ROOT_DIR / "index.html").read_text(encoding="utf-8")
    assert 'id="mlops-lineage-section"' in index_html


def test_m10_monthend_staging_and_ingestion():
    """Validerer integrasjonen av M10 Month-End pakken, staging queue og push-button innlesing."""
    # 1. Sjekk at antigravity_m10_monthend_pack og staging-filer eksisterer
    pack_dir = ROOT_DIR / "antigravity_m10_monthend_pack"
    assert pack_dir.exists(), "antigravity_m10_monthend_pack mangler"
    assert (pack_dir / "ANTIGRAVITY_M10_MonthEnd_Monitoring_and_Staging.md").exists()
    assert (pack_dir / "M10_Oktober_2026_Regnskap_Fiktiv.csv").exists()

    staging_csv = ROOT_DIR / "erp_data" / "staging" / "M10_Oktober_2026_Regnskap_Fiktiv.csv"
    assert staging_csv.exists(), "erp_data/staging CSV mangler"
    lines = staging_csv.read_text(encoding="utf-8-sig").strip().splitlines()
    assert len(lines) == 11, f"Ventet 11 linjer (header + 10 rader), fant {len(lines)}"

    # 2. Test staging status og webhook fra hub_api_server
    from hub_api_server import (
        get_m10_staging_status,
        handle_m10_month_end_webhook,
        execute_m10_ingestion
    )

    status = get_m10_staging_status()
    assert status["ok"] is True
    assert status["file_exists"] is True
    assert status["records_count"] == 10
    assert len(status["file_sha256"]) == 64

    webhook_res = handle_m10_month_end_webhook({"periode": "2026-M10", "event": "month_close.completed"})
    assert webhook_res["ok"] is True
    assert webhook_res["status"] == "ACCEPTED"

    # 3. Test saksbehandler push-button trigger & SHA-256 forsegling
    exec_res = execute_m10_ingestion({
        "periode": "2026-M10",
        "approved_by": "frank.ellingsen@kristiansand.kommune.no",
        "role": "Senior_Controller"
    })
    assert exec_res["ok"] is True
    assert exec_res["status"] == "COMPLETED"
    assert exec_res["records_ingested"] == 10
    assert len(exec_res["sha256_audit_seal"]) == 64

    # 4. Test at m10_ingestion_runner fungerer
    from m10_ingestion_runner import check_status, execute_ingestion
    runner_status = check_status()
    assert runner_status["file_exists"] is True
    assert runner_status["records_count"] == 10

    runner_exec = execute_ingestion()
    assert runner_exec["ok"] is True
    assert runner_exec["status"] == "COMPLETED"
    assert len(runner_exec["sha256_audit_seal"]) == 64

    # 5. Sjekk at index.html har M10 staging banner og triggerfunksjon
    index_html = (ROOT_DIR / "index.html").read_text(encoding="utf-8")
    assert 'id="m10-staging-banner"' in index_html
    assert 'id="btn-m10-trigger"' in index_html
    assert "triggerM10Ingestion" in index_html


def test_triage_router_and_fast_path_classification():
    """Validerer at app/core/triage_router.py og app/schemas/triage.py er fullt operative."""
    from app.schemas.triage import TriageRequest, TriageCategory, ExecutionPriority
    from app.core.triage_router import TriageRouter

    router = TriageRouter()
    
    # 1. RAG lookup test
    req_rag = TriageRequest(
        prompt="Hva sier Kommuneloven § 14-5 om overskridelse av årsbudsjett?",
        session_id="master-test-rag",
        user_persona="CONTROLLER"
    )
    dec_rag = router.classify_and_route_sync(req_rag)
    assert dec_rag.primary_category == TriageCategory.RAG_LOOKUP
    assert len(dec_rag.sha256_audit_hash) == 64

    # 2. Direct MCP test
    req_mcp = TriageRequest(
        prompt="Hent regnskap og visma saldo for Enhet 202.",
        session_id="master-test-mcp",
        user_persona="ENHETSLEDER"
    )
    dec_mcp = router.classify_and_route_sync(req_mcp)
    assert dec_mcp.primary_category == TriageCategory.DIRECT_MCP
    assert "visma_erp" in dec_mcp.required_mcp_connectors

    # 3. Hybrid skill test
    req_skill = TriageRequest(
        prompt="Kjør ompostering for IT-lisenser og sjekk MVA-balansen i Visma.",
        session_id="master-test-hybrid",
        user_persona="CONTROLLER"
    )
    dec_skill = router.classify_and_route_sync(req_skill)
    assert dec_skill.primary_category in [TriageCategory.HYBRID_COMPOSITE, TriageCategory.SKILL_WORKFLOW]
    assert len(dec_skill.sha256_audit_hash) == 64


def test_mva_validering_ci_and_konto_2130_balance():
    """Validerer Momskompensasjonsloven og automatisk avstemming mot Balansekonto 2130."""
    from tools.mva_balanse_validator import verify_mva_balanse_2130

    excel_file = ROOT_DIR / "data" / "repostings" / "Ompostering_Korreksjonsfil_ERP_Eksport_v2.xlsx"
    assert excel_file.exists(), "Korreksjonsfil mangler i data/repostings/"

    res = verify_mva_balanse_2130(str(excel_file))
    assert res["Status"] == "PASSED"
    assert res["Differanse_NOK"] == 0.00
    assert res["Total_Beregnet_MVA_Kompensasjon_NOK"] == 20400.00
    assert res["Ført_Balansekonto_2130_NOK"] == 20400.00
    assert len(res["SHA256_Checksum"]) == 64

    # Sjekk GitHub Actions workflow fil
    workflow_file = ROOT_DIR / ".github" / "workflows" / "mva_validering_ci.yml"
    assert workflow_file.exists()
    assert "tools/mva_balanse_validator.py" in workflow_file.read_text(encoding="utf-8")


def test_cash_management_pakke_and_engine_integration():
    """Validerer at antigravity_cash_management_pakke er implementert og operativ."""
    pack_dir = ROOT_DIR / "antigravity_cash_management_pakke"
    assert pack_dir.exists(), "antigravity_cash_management_pakke mangler"
    assert (pack_dir / "ANTIGRAVITY_Cash_Management_Modul_Spesifikasjon.md").exists()
    assert (pack_dir / "Likviditetsprognose_2026_M11.csv").exists()
    assert (pack_dir / "cash_engine.py").exists()

    from app.services.cash_engine import CashManagementEngine
    from app.schemas.cash import CashPosition, CashSimulationScenario

    engine = CashManagementEngine()
    pos = engine.get_current_position()
    assert pos.credit_facility_limit_nok == 150_000_000.0
    assert pos.bank_balance_nok > 0

    forecast = engine.get_daily_forecast()
    assert len(forecast) == 30
    assert any(f.credit_draw_nok > 0 for f in forecast)

    sim = engine.simulate_scenario(CashSimulationScenario(
        scenario_name="Master Test Scenario",
        tax_revenue_delta_percent=-5.0,
        state_grant_delay_days=5,
        extraordinary_expense_nok=2_500_000.0,
    ))
    assert len(sim.sha256_audit_seal) == 64
    assert sim.days_in_overdraft > 0


def test_top3_kpi_and_report_export_packages_integration():
    """Validerer integrasjonen av antigravity_top3_kpi_visualisering_pakke og antigravity_report_export_pakke."""
    # 1. Valider Top 3 KPI-pakke
    kpi_dir = ROOT_DIR / "antigravity_top3_kpi_visualisering_pakke"
    assert kpi_dir.exists(), "antigravity_top3_kpi_visualisering_pakke mangler"
    assert (kpi_dir / "ANTIGRAVITY_Top3_KPI_Visualisering_og_Hierarki.md").exists()
    assert (kpi_dir / "Top3_KPI_Gauge_Dashboard_Data.json").exists()

    from app.services.top3_kpi_service import Top3KpiService
    svc = Top3KpiService()
    kpi_payload = svc.get_dashboard_payload()
    assert kpi_payload.kommune == "Kristiansand kommune"
    assert len(kpi_payload.top3_kpis) == 3
    assert len(kpi_payload.budsjetthierarki) >= 3

    # 2. Valider Report Export Engine-pakke
    export_dir = ROOT_DIR / "antigravity_report_export_pakke"
    assert export_dir.exists(), "antigravity_report_export_pakke mangler"
    assert (export_dir / "ANTIGRAVITY_Automated_Report_Export_Engine.md").exists()
    assert (export_dir / "export_bystyret_report.py").exists()

    from app.services.report_export_engine import generate_bystyret_pptx
    res = generate_bystyret_pptx()
    assert res["ok"] is True
    assert res["slides_count"] == 4
    assert Path(res["file_path"]).exists()
    assert len(res["sha256_audit_seal"]) == 64


def test_evaluation_database_and_ai_engineering_agents_integration():
    """Validerer integrasjonen av agentene 13, 14 og 15 (Evaluering, Database og AI Engineering)."""
    agenter_dir = ROOT_DIR / "agenter"
    assert (agenter_dir / "13_evaluering_kvalitetssikring_agent.md").exists()
    assert (agenter_dir / "14_database_data_engineering_agent.md").exists()
    assert (agenter_dir / "15_ai_engineering_infrastruktur_agent.md").exists()

    # 1. Agent 13: Evaluation Service
    from app.services.evaluation_service import EvaluationService
    eval_svc = EvaluationService()
    rep = eval_svc.run_golden_suite()
    assert rep.total_tests >= 5
    assert rep.overall_faithfulness >= 0.90
    assert rep.ci_cd_gate_passed is True

    # 2. Agent 14: Database Service
    from app.services.database_agent_service import DatabaseAgentService
    from app.schemas.database import QueryRequest
    db_svc = DatabaseAgentService()
    schema = db_svc.inspect_schema()
    assert len(schema["tables"]) >= 5
    q_res = db_svc.execute_query(QueryRequest(sql="SELECT 1 AS num;"))
    assert q_res.rows[0]["num"] == 1

    # 3. Agent 15: AI Engineering Service
    from app.services.ai_engineering_service import AIEngineeringService
    aie_svc = AIEngineeringService()
    status = aie_svc.get_4_layer_status()
    assert status.framework_layer["agents_count"] == 15
    assert status.harness_layer["max_steps"] == 10


def test_municipal_advisor_knowledge_and_vector_expansion():
    """Validerer utvidelsen av kunnskapsbasen for kommunale økonomirådgivere (Vektor-DB & Hub)."""
    import json
    from pathlib import Path
    import sqlite3

    json_path = ROOT_DIR / "erp_data" / "municipal_advisor_knowledge_chunks.json"
    assert json_path.exists(), "Fant ikke municipal_advisor_knowledge_chunks.json"

    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    assert len(chunks) >= 30, f"Forventet minst 30 kunnskapsmoduler, fant {len(chunks)}"
    categories = {c["category"] for c in chunks}
    assert "Delegering & Fullmakter" in categories
    assert "Framsikt & Lønn" in categories
    assert "Selvkost & VAR" in categories
    assert "MVA & Momskompensasjon" in categories
    assert "Statlige Tilskudd" in categories

    # 1. Test Golden Record DB
    golden_db = ROOT_DIR / "erp_data" / "kommune_golden_record.db"
    assert golden_db.exists()
    conn = sqlite3.connect(str(golden_db))
    cur = conn.cursor()
    cnt = cur.execute("SELECT count(*) FROM legal_chunks").fetchone()[0]
    assert cnt >= 170, f"Forventet minst 170 rader i legal_chunks, fant {cnt}"
    fts_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='legal_fts'").fetchone()
    assert fts_check is not None, "legal_fts tabell mangler i golden record"
    conn.close()

    # 2. Test MCP search_municipal_law
    from kommune_ai_guardrails.mcp_server import search_municipal_law
    selvkost_res = search_municipal_law("kalkylerente selvkost swap", top_k=2)
    assert len(selvkost_res) > 0
    assert any("selvkost" in str(r).lower() for r in selvkost_res)

    mva_res = search_municipal_law("mva justering 10 år konto 2130", top_k=2)
    assert len(mva_res) > 0
    assert any("mva" in str(r).lower() or "moms" in str(r).lower() for r in mva_res)

    # 3. Test Hub API rådgiver-endepunkter
    from tools.hub_api_server import get_v1_advisor_faq, search_v1_advisor
    faq = get_v1_advisor_faq()
    assert faq["ok"] is True
    assert faq["total"] >= 30

    search_res = search_v1_advisor({"query": "omdisponering vikar"})
    assert search_res["ok"] is True
    assert len(search_res["results"]) > 0







