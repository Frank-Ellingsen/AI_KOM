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

