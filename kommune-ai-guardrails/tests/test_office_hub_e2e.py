"""End-to-End (A-to-Z) Test Suite for Kristiansand Kommune Control Office Hub.

Tests:
1. Document catalog integrity (all 133 paths in DOCUMENTS_MENU exist on disk).
2. Golden Record EVM & KOSTRA variance queries (ISO 21508 formulas, CTE pre-aggregation).
3. MCP Server tool orchestration across all intent categories (financials + law + EOY impact, kontoutskrift, navigation).
4. Stage-Gate Port 4 (PII scrubbing incl. D-numbers) & Stage-Gate Port 9/10 (HITL SHA-256 SQLite logging).
5. Static HTML Office Hub (app/static/index.html) structural & client-side guardrail verification.
"""

import hashlib
import datetime
from pathlib import Path
import pytest

from kommune_ai_guardrails.rag import get_db_connection, init_audit_log, sanitize_pii
from kommune_ai_guardrails.mcp_server import (
    execute_gemini_mcp_query,
    get_unit_financials,
    search_municipal_law,
    calculate_eoy_impact,
    locate_hub_resource,
)

HUB_APP_PATH = Path(__file__).resolve().parents[1] / "app" / "app.py"
STATIC_HTML_PATH = Path(__file__).resolve().parents[1] / "app" / "static" / "index.html"


def test_app_py_compiles_and_all_133_documents_exist():
    """Verify app/app.py compiles cleanly and 100% of DOCUMENTS_MENU files exist on disk."""
    assert HUB_APP_PATH.exists(), f"Missing {HUB_APP_PATH}"
    source = HUB_APP_PATH.read_text(encoding="utf-8")
    compile(source, str(HUB_APP_PATH), "exec")

    import sys
    app_dir = str(HUB_APP_PATH.parent)
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    import app as hub_app

    total_docs = 0
    missing_docs = []
    for cat_title, items in hub_app.DOCUMENTS_MENU.items():
        for label, path, desc in items:
            total_docs += 1
            if not Path(path).exists():
                missing_docs.append((cat_title, label, str(path)))

    assert total_docs >= 133, f"Expected at least 133 documents in DOCUMENTS_MENU, got {total_docs}"
    assert missing_docs == [], f"Found broken paths in DOCUMENTS_MENU: {missing_docs}"


def test_office_hub_database_and_evm_calculations():
    """Verify Golden Record EVM consolidation and KOSTRA variance queries."""
    import sys
    app_dir = str(HUB_APP_PATH.parent)
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    import app as hub_app

    stats = hub_app.get_db_stats()
    assert stats["chunks"] > 3000, f"Expected >3000 legal chunks in RAG store, got {stats['chunks']}"
    assert stats["audits"] >= 0
    assert stats["regnskap_rader"] > 1000, f"Expected >1000 rows in Fact_Regnskap, got {stats['regnskap_rader']}"
    assert stats["budsjett_rader"] > 1000, f"Expected >1000 rows in Fact_Budsjett, got {stats['budsjett_rader']}"

    df_evm = hub_app.load_golden_record_evm()
    assert not df_evm.empty, "load_golden_record_evm() returned an empty DataFrame"
    assert len(df_evm) >= 40, f"Expected at least 40 units in Golden Record EVM, got {len(df_evm)}"

    # Verify ISO 21508 EVM identities on the first row
    row = df_evm.iloc[0]
    pv = float(row["Planlagt (PV)"])
    ac = float(row["Påløpt (AC)"])
    cv = float(row["Avvik (CV)"])
    cpi = float(row["CPI"])
    bac = float(row["Årsbudsjett (BAC)"])
    eac = float(row["Sluttprognose (EAC)"])

    assert abs(cv - (pv - ac)) < 1.0, f"CV ({cv}) != PV - AC ({pv - ac})"
    if ac > 0:
        assert abs(cpi - round(pv / ac, 3)) <= 0.002
    if cpi > 0:
        assert abs(eac - (bac / (pv / ac))) / max(bac, 1.0) < 0.01

    # Verify top cost variances across all units and filtered by a specific unit
    df_var_all = hub_app.load_top_cost_variances("Alle Enheter")
    assert not df_var_all.empty, "load_top_cost_variances('Alle Enheter') should not be empty"
    assert len(df_var_all) <= 10

    first_unit = str(df_evm.iloc[0]["Enhet"])
    df_var_unit = hub_app.load_top_cost_variances(first_unit)
    assert isinstance(df_var_unit, type(df_var_all))


def test_stage_gate_port4_pii_and_port9_hitl_signoff():
    """Verify Stage-Gate Port 4 PII scrubbing and Port 9 HITL SHA-256 SQLite logging."""
    raw_input = (
        "Saksbehandler med FNR 12058512345 og D-nr 52058512345, "
        "tlf +47 987 65 432, e-post frank.ellingsen@kristiansand.kommune.no."
    )
    scrubbed = sanitize_pii(raw_input)
    assert "12058512345" not in scrubbed
    assert "52058512345" not in scrubbed
    assert "987 65 432" not in scrubbed
    assert "frank.ellingsen@kristiansand.kommune.no" not in scrubbed
    assert "[SKJERMET FNR]" in scrubbed
    assert "[SKJERMET TLF]" in scrubbed
    assert "[SKJERMET E-POST]" in scrubbed

    # Verify Stage-Gate Port 9 HITL SQLite insert matches schema
    conn = get_db_connection()
    init_audit_log(conn)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    sakstype = "Sak: 2. Tertialrapport 2026 — E2E Test"
    hitl_status = "APPROVED (Godkjent)"
    hitl_notes = "Verifisert av automatisk E2E-test for Stage-Gate Port 9."
    raw_payload = f"Økonomicontroller|{sakstype}|{hitl_status}|{hitl_notes}|{timestamp}"
    audit_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()

    conn.execute(
        """
        INSERT INTO Audit_AI_Actions (user_query, retrieved_chunk_ids, llm_response, action_type, sha256_hash, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (sakstype, "[]", hitl_notes, f"HITL_{hitl_status.split()[0]}", audit_hash, timestamp),
    )
    conn.commit()

    row = conn.execute(
        "SELECT action_type, sha256_hash FROM Audit_AI_Actions WHERE sha256_hash = ?",
        (audit_hash,),
    ).fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "HITL_APPROVED"
    assert row[1] == audit_hash


def test_mcp_server_all_intents_end_to_end():
    """Verify MCP tool routing across financials + law + EOY impact, kontoutskrift, and navigation."""
    # 1. Financials + Law + EOY impact intent
    res_fin = execute_gemini_mcp_query("Hva er avviket på vikar og overtid for Kommunal Skole jf. § 14-5?")
    assert res_fin["audit_hash"] and len(res_fin["audit_hash"]) == 64
    called_fin = " ".join(res_fin["tools_called"])
    assert "get_unit_financials" in called_fin
    assert "search_municipal_law" in called_fin
    assert "calculate_eoy_impact" in called_fin

    # 2. Kontoutskrift intent
    res_konto = execute_gemini_mcp_query("Vis kontoutskrift og saldo for 5200 Bo og Miljø")
    called_konto = " ".join(res_konto["tools_called"])
    assert "locate_hub_resource" in called_konto
    assert "kontoutskrift" in called_konto
    assert len(res_konto["audit_hash"]) == 64

    # 3. Document library / Power BI navigation intent
    res_nav = execute_gemini_mcp_query("Hvor finner jeg Power BI rapport for Oppvekst?")
    called_nav = " ".join(res_nav["tools_called"])
    assert "locate_hub_resource" in called_nav
    assert len(res_nav["audit_hash"]) == 64


def test_static_html_office_hub_integrity():
    """Verify app/static/index.html contains Tufte styling, client-side PII guardrails, and dynamic filter logic."""
    assert STATIC_HTML_PATH.exists(), f"Missing {STATIC_HTML_PATH}"
    html_text = STATIC_HTML_PATH.read_text(encoding="utf-8")

    for required_token in [
        "EDWARD TUFTE DATA-INK RATIO DESIGN SYSTEM",
        "tufte-table",
        "sanitizePIIClient",
        "executeMockRAG",
        "filterEntity",
        "variances-tbody",
        "TOTALT TOPP 4 AVVIK (SKOLE)",
        "exportAuditTrail",
        "toggleEngine",
    ]:
        assert required_token in html_text, f"Expected '{required_token}' in app/static/index.html"
