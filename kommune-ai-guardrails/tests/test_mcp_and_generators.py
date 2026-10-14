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
from kommune_ai_guardrails.generators.powerpoint_generator import (
    generate_bystyret_deck,
    generate_konsern_deck,
    generate_oppvekst_deck,
    generate_capex_evm_deck,
    generate_enhet202_deck,
)
from kommune_ai_guardrails.generators.excel_fast_generator import generate_fast_excel_model
from kommune_ai_guardrails.generators.excel_evm_generator import generate_project_controller_evm_model
from kommune_ai_guardrails.generators.excel_cfo_generator import generate_cfo_executive_konsern_model
from kommune_ai_guardrails.generators.excel_hr_generator import generate_hr_lonn_vikar_monitor_model
from kommune_ai_guardrails.generators.word_saksfremlegg_generator import (
    generate_saksfremlegg_docx,
    generate_hop_notat_docx,
    generate_raadmann_notat_docx,
    generate_sektornotat_oppvekst_docx,
    generate_prosjektkontroll_capex_docx,
    generate_avviksnotat_enhetsleder_docx,
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
    # 1. Bystyret Deck (Nivå 1)
    target1 = tmp_path / "test_bystyret.pptx"
    out1 = generate_bystyret_deck(output_path=str(target1))
    assert Path(out1).exists()
    assert Path(out1).stat().st_size > 10000

    # 2. Konsernstyring Deck (Nivå 2)
    target2 = tmp_path / "test_konsern.pptx"
    out2 = generate_konsern_deck(output_path=str(target2))
    assert Path(out2).exists()
    assert Path(out2).stat().st_size > 10000

    # 3. Oppvekst Deck (Nivå 3)
    target3 = tmp_path / "test_oppvekst.pptx"
    out3 = generate_oppvekst_deck(output_path=str(target3))
    assert Path(out3).exists()
    assert Path(out3).stat().st_size > 10000

    # 4. Capex EVM Deck (Nivå 4)
    target4 = tmp_path / "test_capex_evm.pptx"
    out4 = generate_capex_evm_deck(output_path=str(target4))
    assert Path(out4).exists()
    assert Path(out4).stat().st_size > 10000

    # 5. Enhet 202 Deck (Nivå 5)
    target5 = tmp_path / "test_enhet202.pptx"
    out5 = generate_enhet202_deck(output_path=str(target5))
    assert Path(out5).exists()
    assert Path(out5).stat().st_size > 10000


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
    # 1. Bystyret Saksfremlegg (Nivå 1)
    doc1 = tmp_path / "test_saksfremlegg.docx"
    out1 = generate_saksfremlegg_docx(output_path=str(doc1))
    assert Path(out1).exists()
    assert Path(out1).stat().st_size > 10000

    # 2. HØP Notat (Nivå 2)
    doc2 = tmp_path / "test_hop.docx"
    out2 = generate_hop_notat_docx(output_path=str(doc2))
    assert Path(out2).exists()
    assert Path(out2).stat().st_size > 10000

    # 3. Rådmann Strakstiltak (Nivå 2)
    doc3 = tmp_path / "test_raadmann.docx"
    out3 = generate_raadmann_notat_docx(output_path=str(doc3))
    assert Path(out3).exists()
    assert Path(out3).stat().st_size > 10000

    # 4. Sektorstyring Oppvekst (Nivå 3)
    doc4 = tmp_path / "test_oppvekst.docx"
    out4 = generate_sektornotat_oppvekst_docx(output_path=str(doc4))
    assert Path(out4).exists()
    assert Path(out4).stat().st_size > 10000

    # 5. Capex Statusnotat EVM (Nivå 4)
    doc5 = tmp_path / "test_capex.docx"
    out5 = generate_prosjektkontroll_capex_docx(output_path=str(doc5))
    assert Path(out5).exists()
    assert Path(out5).stat().st_size > 10000

    # 6. Avviksnotat Enhetsleder (Nivå 5)
    doc6 = tmp_path / "test_enhetsleder.docx"
    out6 = generate_avviksnotat_enhetsleder_docx(output_path=str(doc6))
    assert Path(out6).exists()
    assert Path(out6).stat().st_size > 10000


def test_powerbi_pbip_generator():
    res = build_pbip_project()
    assert res["status"] == "SUCCESS"
    assert res["pages_count"] == 7
    assert res["visuals_count"] >= 40
    assert res["tables_count"] >= 8
    assert Path(res["pbip_file"]).exists()
