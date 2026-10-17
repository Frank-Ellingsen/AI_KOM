"""
Pytest integration for MVA Balansekonto 2130 Validering
Kristiansand Kommune — Kvalitetskontroll for momskompensasjon.
"""

from pathlib import Path
import pytest
from tools.mva_balanse_validator import verify_mva_balanse_2130

ROOT_DIR = Path(__file__).resolve().parent.parent
EXCEL_PATH = ROOT_DIR / "data" / "repostings" / "Ompostering_Korreksjonsfil_ERP_Eksport_v2.xlsx"


def test_mva_balansekonto_2130_verification():
    """Tester at korreksjonsfil har 0.00 i avvik mellom beregnet MVA og Balansekonto 2130."""
    assert EXCEL_PATH.exists(), f"Mangler korreksjonsfil: {EXCEL_PATH}"
    res = verify_mva_balanse_2130(str(EXCEL_PATH))

    assert res["Status"] == "PASSED"
    assert res["Differanse_NOK"] == 0.00
    assert res["Total_Beregnet_MVA_Kompensasjon_NOK"] == 20400.00
    assert res["Ført_Balansekonto_2130_NOK"] == 20400.00
    assert len(res["SHA256_Checksum"]) == 64
    assert res["Antall_Behandlede_Linjer"] == 4
