"""
Test Suite for Top 3 KPIs and Cascading Budget Hierarchy
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.schemas.kpi import Top3KpiDashboardResponse
from app.services.top3_kpi_service import Top3KpiService


def test_top3_kpi_service_data_loading():
    """Tester at Top3KpiService laster inn JSON-data og produserer Pydantic-modeller."""
    svc = Top3KpiService()
    payload = svc.get_dashboard_payload()

    assert isinstance(payload, Top3KpiDashboardResponse)
    assert payload.kommune == "Kristiansand kommune"
    assert "netto_driftsresultat" in payload.top3_kpis
    assert "disposisjonsfond" in payload.top3_kpis
    assert "netto_lånegjeld" in payload.top3_kpis

    # Sjekk verdier mot TBU og kommunale mål
    driftsresultat = payload.top3_kpis["netto_driftsresultat"]
    assert driftsresultat.verdi == 1.25
    assert driftsresultat.mål_kommune == 1.00
    assert driftsresultat.status == "GRØNN"

    fond = payload.top3_kpis["disposisjonsfond"]
    assert fond.verdi == 4.35
    assert fond.mål_kommune == 4.00

    gjeld = payload.top3_kpis["netto_lånegjeld"]
    assert gjeld.verdi == 76.8
    assert gjeld.mål_kommune == 78.0


def test_budget_hierarchy_drilldown():
    """Tester at budsjetthierarkiet har korrekte sektorer og enhets-KPIer."""
    svc = Top3KpiService()
    hierarchy = svc.get_hierarchy()

    assert len(hierarchy) >= 3
    sektorer = {s.sektor_id: s for s in hierarchy}

    assert "OMR-02" in sektorer  # Oppvekst
    assert "OMR-03" in sektorer  # Helse og Mestring
    assert "OMR-05" in sektorer  # By- og Stedsutvikling

    oppvekst = sektorer["OMR-02"]
    assert oppvekst.avvik_ytd_nok == 35000000.0
    assert oppvekst.triage_status == "RØD"
    assert "pedagogdekning_prosent" in oppvekst.sektor_spesifikke_kpis

    byutvikling = sektorer["OMR-05"]
    assert byutvikling.sektor_spesifikke_kpis["var_selvkostgrad_prosent"] == 100.0


def test_hub_api_server_kpi_endpoints():
    """Tester at hub_api_server serverer KPI- og hierarkiendepunkter."""
    from tools.hub_api_server import get_v1_top3_kpis, get_v1_kpi_hierarchy

    kpis = get_v1_top3_kpis()
    assert kpis["ok"] is True
    assert "netto_driftsresultat" in kpis["top3_kpis"]
    assert len(kpis["sha256_audit_seal"]) == 64

    hier = get_v1_kpi_hierarchy()
    assert hier["ok"] is True
    assert len(hier["budsjetthierarki"]) >= 3


def test_kpi_runner_cli():
    """Tester at tools/kpi_runner.py eksekverer feilfritt via CLI."""
    cmd = [sys.executable, str(ROOT_DIR / "tools" / "kpi_runner.py"), "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert "top3_kpis" in data
