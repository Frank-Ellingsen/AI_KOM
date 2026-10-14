"""
Tester for Gemini Flash MCP Server og dokumentgeneratorer (PowerPoint, Excel, Word).
"""
import os
from pathlib import Path
import pytest

from kommune_ai_guardrails.mcp_server import (
    get_unit_financials,
    search_municipal_law,
    calculate_eoy_impact,
    execute_gemini_mcp_query
)
from kommune_ai_guardrails.generators.powerpoint_generator import generate_bystyret_deck
from kommune_ai_guardrails.generators.excel_fast_generator import generate_fast_excel_model
from kommune_ai_guardrails.generators.excel_evm_generator import generate_project_controller_evm_model
from kommune_ai_guardrails.generators.excel_cfo_generator import generate_cfo_executive_konsern_model
from kommune_ai_guardrails.generators.excel_hr_generator import generate_hr_lonn_vikar_monitor_model
from kommune_ai_guardrails.generators.word_saksfremlegg_generator import (
    generate_saksfremlegg_docx,
    generate_hop_notat_docx
)
from kommune_ai_guardrails.generators.powerbi_pbip_generator import build_pbip_project


def test_mcp_get_unit_financials():
    data = get_unit_financials(unit_id="202", period="Q2")
    assert data["unit_id"] == "202"
    assert "variance_nok" in data
    assert "top_variance_accounts" in data
    assert len(data["top_variance_accounts"]) > 0


def test_mcp_search_municipal_law():
    laws = search_municipal_law("Kommuneloven § 14-5 inndekning merforbruk", top_k=2)
    assert len(laws) > 0
    paragrafer = [l["paragraf"] for l in laws]
    assert any("14-5" in p for p in paragrafer)


def test_mcp_calculate_eoy_impact():
    impact = calculate_eoy_impact(unit_id="202", action_type="vikar_stopp", monthly_saving=170000.0, start_month=8)
    assert impact["unit_id"] == "202"
    assert impact["prognosis_without_action_p90"] > impact["prognosis_with_action_p10"]
    assert impact["fund_coverage_possible"] is True


def test_mcp_execute_gemini_query():
    query = "Hva er status på Enhet 202 Grunnskole per Q2 og hva er helårseffekten?"
    result = execute_gemini_mcp_query(query)
    assert "text" in result
    assert "audit_hash" in result
    assert len(result["audit_hash"]) == 64  # SHA-256 length
    # Sjekk 4-punkts strukturen
    assert "1. Avvik hittil i år" in result["text"]
    assert "2. Årsak til avvik" in result["text"]
    assert "3. Forslag til Action Plan" in result["text"]
    assert "4. Kvantifisert Effekt" in result["text"]


def test_powerpoint_generator(tmp_path):
    target = tmp_path / "test_presentation.pptx"
    out = generate_bystyret_deck(output_path=str(target))
    assert Path(out).exists()
    assert Path(out).stat().st_size > 10000


def test_excel_generators(tmp_path):
    # 1. FAST Modell
    m1 = tmp_path / "test_fast.xlsx"
    out1 = generate_fast_excel_model(output_path=str(m1))
    assert Path(out1).exists()
    assert Path(out1).stat().st_size > 5000

    # 2. EVM Modell
    m2 = tmp_path / "test_evm.xlsx"
    out2 = generate_project_controller_evm_model(output_path=str(m2))
    assert Path(out2).exists()
    assert Path(out2).stat().st_size > 5000

    # 3. CFO Modell
    m3 = tmp_path / "test_cfo.xlsx"
    out3 = generate_cfo_executive_konsern_model(output_path=str(m3))
    assert Path(out3).exists()
    assert Path(out3).stat().st_size > 5000

    # 4. HR Modell
    m4 = tmp_path / "test_hr.xlsx"
    out4 = generate_hr_lonn_vikar_monitor_model(output_path=str(m4))
    assert Path(out4).exists()
    assert Path(out4).stat().st_size > 5000


def test_word_generators(tmp_path):
    doc1 = tmp_path / "test_saksfremlegg.docx"
    out1 = generate_saksfremlegg_docx(output_path=str(doc1))
    assert Path(out1).exists()
    assert Path(out1).stat().st_size > 10000

    doc2 = tmp_path / "test_hop.docx"
    out2 = generate_hop_notat_docx(output_path=str(doc2))
    assert Path(out2).exists()
    assert Path(out2).stat().st_size > 10000


def test_powerbi_pbip_generator():
    res = build_pbip_project()
    assert res["status"] == "SUCCESS"
    assert res["pages_count"] == 7
    assert res["visuals_count"] >= 40
    assert res["tables_count"] >= 8
    assert Path(res["pbip_file"]).exists()
