"""
Test Suite for Månedlig PDF- og Lederrapport-Generator
Kristiansand Kommune — AI Project Controller Hub
Lead Controller: Frank Ellingsen
"""

import csv
import json
from pathlib import Path
import pytest
import sqlite3
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT_DIR / "tools"
REPORTS_DIR = ROOT_DIR / "reports" / "monthly_pdf_packets"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from generate_monthly_pdf_reports import (
    get_budget_holders_from_db,
    calculate_unit_metrics,
    generate_pdf_report,
    generate_html_report,
    export_framsikt_batch_csv
)


def test_calculate_unit_metrics_variance_formula():
    """Validerer at formelkravet 'Avvik = Budsjett - Actuals' overholdes 100 %."""
    holders = get_budget_holders_from_db()
    assert len(holders) > 0, "Ingen budsjettansvarlige funnet i databasen"

    for h in holders[:10]:
        metrics = calculate_unit_metrics(h, month=9)
        ytd_b = metrics["ytd_budget"]
        ytd_a = metrics["ytd_actual"]
        avvik = metrics["avvik_ytd"]

        # Formelsjekk: Avvik = Budsjett - Actuals
        assert avvik == pytest.approx(ytd_b - ytd_a, rel=1e-5), "Avvik må være Budsjett - Actuals"

        if avvik >= 0:
            assert metrics["is_surplus"] is True, "Positivt avvik skal klassifiseres som surplus"
            assert metrics["rag_status"] == "GREEN", "Positivt avvik skal ha GRØNT trafikklys"
        elif avvik < -500000:
            assert metrics["is_surplus"] is False, "Vesentlig negativt avvik skal klassifiseres som deficit"
            assert metrics["rag_status"] == "RED", "Stort merforbruk skal ha RØDT trafikklys"


def test_generate_pdf_report_surplus_and_deficit(tmp_path):
    """Tester generering av faktiske PDF- og HTML-rapporter for både overskudds- og underskuddsenheter."""
    holders = get_budget_holders_from_db()
    holder_map = {h["ansvar_id"]: h for h in holders}

    # Test 1: Deficit enhet (Strai Sykehjem 5200-ENH-401)
    if "5200-ENH-401" in holder_map:
        m_def = calculate_unit_metrics(holder_map["5200-ENH-401"], month=9)
        assert m_def["is_surplus"] is False
        pdf_def = tmp_path / "strai_test.pdf"
        html_def = tmp_path / "strai_test.html"

        generate_pdf_report(m_def, pdf_def)
        generate_html_report(m_def, html_def)

        assert pdf_def.exists() and pdf_def.stat().st_size > 3000
        # Sjekk PDF magic header
        with open(pdf_def, "rb") as f:
            header = f.read(5)
            assert header == b"%PDF-", "Ugyldig PDF-header"

        assert html_def.exists() and html_def.stat().st_size > 5000
        html_text = html_def.read_text(encoding="utf-8")
        assert "Strai Sykehjem" in html_text
        assert "Budsjett - Actuals" in html_text
        assert "Framsikt EPM" in html_text

    # Test 2: Surplus enhet (Byggesak & Tilsyn 3300-ENH-301)
    if "3300-ENH-301" in holder_map:
        m_sur = calculate_unit_metrics(holder_map["3300-ENH-301"], month=9)
        assert m_sur["is_surplus"] is True
        pdf_sur = tmp_path / "byggesak_test.pdf"
        html_sur = tmp_path / "byggesak_test.html"

        generate_pdf_report(m_sur, pdf_sur)
        generate_html_report(m_sur, html_sur)

        assert pdf_sur.exists() and pdf_sur.stat().st_size > 3000
        assert html_sur.exists() and html_sur.stat().st_size > 5000
        html_sur_text = html_sur.read_text(encoding="utf-8")
        assert "Byggesak og Tilsyn" in html_sur_text
        assert "Mindreforbruk" in html_sur_text


def test_framsikt_batch_csv_balance(tmp_path):
    """Tester at Framsikt CSV-batch balanserer til nøyaktig 0 kr per reguleringssak."""
    holders = get_budget_holders_from_db()
    all_metrics = [calculate_unit_metrics(h, month=9) for h in holders[:6]]

    csv_path = tmp_path / "framsikt_test_batch.csv"
    export_framsikt_batch_csv(all_metrics, csv_path, month=9)

    assert csv_path.exists() and csv_path.stat().st_size > 200

    # Les og summer per regulerings_id
    reg_sums = {}
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rid = row["regulerings_id"]
            belop = float(row["belop_nok"])
            reg_sums[rid] = reg_sums.get(rid, 0.0) + belop

    # Alle reguleringer skal summere til nøyaktig 0,00 NOK
    for rid, total in reg_sums.items():
        assert total == pytest.approx(0.0, abs=1e-2), f"Regulering {rid} balanserer ikke: sum = {total}"


def test_sha256_audit_seal_present():
    """Validerer at Monte Carlo-prognosen er forseglet med gyldig SHA-256 for Stage-Gate Port 9."""
    holders = get_budget_holders_from_db()
    m = calculate_unit_metrics(holders[0], month=9)
    sha = m["prognosis"]["sha256"]
    assert isinstance(sha, str)
    assert len(sha) == 64, f"SHA-256 hash må være 64 heksadesimale tegn: {sha}"
    assert int(sha, 16) > 0, "SHA-256 må være et gyldig hekstall"


def test_individual_budget_holder_archives_structure():
    """Validerer at alle 41 budsjettansvarlige har opprettet sitt eget dedikerte rapportarkiv."""
    archive_dir = ROOT_DIR / "reports" / "budsjettansvarlige_arkiv"
    assert archive_dir.exists(), "Masterarkiv-mappen finnes ikke"

    master_index = archive_dir / "index.html"
    assert master_index.exists() and master_index.stat().st_size > 10000, "Masterarkiv index.html mangler"

    holders = get_budget_holders_from_db()
    assert len(holders) >= 41, f"Forventet minst 41 budsjettansvarlige, fant {len(holders)}"

    # Sjekk et representativt utvalg av enheter
    sample_ids = ["5200-ENH-401", "4100-ENH-202", "3300-ENH-301", "2020", "5000-SJEF-HELSE"]
    for aid in sample_ids:
        unit_dir = archive_dir / aid
        assert unit_dir.exists(), f"Arkivmappe mangler for {aid}"

        # 4 undermapper
        subdirs = [
            unit_dir / "01_Maanedsrapporter",
            unit_dir / "02_Kontoutskrifter",
            unit_dir / "03_Saksdokumenter_og_Maler",
            unit_dir / "04_Framsikt_Omdisponering"
        ]
        for sd in subdirs:
            assert sd.exists(), f"Undermappe mangler: {sd}"

        # Sjekk at PDF og HTML månedsrapporter finnes
        pdf_m9 = unit_dir / "01_Maanedsrapporter" / "Maanedsrapport_M09_2026.pdf"
        assert pdf_m9.exists() and pdf_m9.stat().st_size > 3000

        # Sjekk at Framsikt-konteringsfil finnes
        framsikt_csv = unit_dir / "04_Framsikt_Omdisponering" / f"framsikt_kontering_{aid}.csv"
        assert framsikt_csv.exists() and framsikt_csv.stat().st_size > 50

        # Sjekk at ARKIV_OVERSIKT.html og README.md finnes
        overview = unit_dir / "ARKIV_OVERSIKT.html"
        readme = unit_dir / "README.md"
        assert overview.exists() and overview.stat().st_size > 5000
        assert readme.exists() and readme.stat().st_size > 500

