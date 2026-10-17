"""
Master Test Suite for Cash Management & Likviditetsstyring
jf. Kommuneloven §§ 14-1, 14-13, 14-14, 14-15 og Finansforskriften.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import polars as pl

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.schemas.cash import (
    CashPosition,
    DailyCashFlowEntry,
    CashSimulationScenario,
    CashSimulationResult,
    CashComplianceReport,
)
from app.services.cash_engine import CashManagementEngine


def test_pydantic_cash_schemas():
    """Validerer at Pydantic-skjemaene for Cash Management håndhever felter og typer."""
    pos = CashPosition(
        as_of_date="2026-11-01",
        bank_balance_nok=42850000.0,
        credit_facility_limit_nok=150000000.0,
        credit_facility_used_nok=24500000.0,
        available_liquidity_nok=168350000.0,
        utilization_rate_percent=16.33,
        status="CREDIT_DRAW",
    )
    assert pos.bank_balance_nok == 42850000.0
    assert pos.utilization_rate_percent == 16.33

    entry = DailyCashFlowEntry(
        entry_date="2026-11-12",
        inflow_tax_nok=0.0,
        inflow_state_grants_nok=0.0,
        inflow_other_nok=150000.0,
        outflow_payroll_nok=82000000.0,
        outflow_suppliers_nok=1200000.0,
        outflow_debt_service_nok=0.0,
        net_cash_flow_nok=-83050000.0,
        projected_end_balance_nok=-6750000.0,
        credit_draw_nok=6750000.0,
        available_credit_remaining_nok=143250000.0,
        status="UTILIZING_CREDIT",
    )
    assert entry.credit_draw_nok == 6750000.0
    assert entry.status == "UTILIZING_CREDIT"


def test_cash_engine_forecast_and_polars():
    """Tester kjerneberegningene i CashManagementEngine med Polars og CSV."""
    engine = CashManagementEngine(credit_limit_nok=150_000_000.0)
    df = engine.process_forecast(initial_balance=42_850_000.0)

    assert isinstance(df, pl.DataFrame)
    assert df.height == 30  # 30 dager i november
    assert "Beregnet_Saldo" in df.columns
    assert "Kassakreditt_Trekk" in df.columns

    # Sjekk at 12. nov har kassakredittrekk på grunn av fastlønn
    nov12 = df.filter(pl.col("Dato") == "2026-11-12")
    assert nov12["Kassakreditt_Trekk"][0] > 0
    assert nov12["Status"][0] == "UTILIZING_CREDIT"

    # Sjekk at 15. nov normaliserer saldoen etter statlig rammetilskudd
    nov15 = df.filter(pl.col("Dato") == "2026-11-15")
    assert nov15["Beregnet_Saldo"][0] > 50_000_000.0
    assert nov15["Kassakreditt_Trekk"][0] == 0.0
    assert nov15["Status"][0] == "OK"


def test_cash_engine_what_if_simulation():
    """Tester scenariesimulering ved skattefall og forsinkelse på rammetilskudd."""
    engine = CashManagementEngine(credit_limit_nok=150_000_000.0)
    scenario = CashSimulationScenario(
        scenario_name="Stress-scenario Snøfall & Skattesvikt",
        tax_revenue_delta_percent=-8.0,
        state_grant_delay_days=7,
        extraordinary_expense_nok=4_500_000.0,
    )
    res = engine.simulate_scenario(scenario)

    assert isinstance(res, CashSimulationResult)
    assert res.simulated_min_balance_nok < res.baseline_min_balance_nok
    assert res.simulated_max_credit_draw_nok > res.baseline_max_credit_draw_nok
    assert len(res.sha256_audit_seal) == 64
    assert res.days_in_overdraft > 0
    assert not res.overdraft_limit_breached  # Fortsatt under 150 mill kr


def test_cash_engine_compliance_report():
    """Tester at Finansforskriften og Kommuneloven § 14-14 valideres korrekt."""
    engine = CashManagementEngine(credit_limit_nok=150_000_000.0)
    rep = engine.check_compliance()

    assert isinstance(rep, CashComplianceReport)
    assert rep.is_within_statutory_limit is True
    assert "14-14" in rep.legal_basis[2]
    assert len(rep.sha256_audit_seal) == 64
    assert "GODKJENT" in rep.compliance_verdict


def test_hub_api_server_cash_endpoints():
    """Tester v1 API-endepunktene for cash management i hub_api_server."""
    from tools.hub_api_server import (
        get_v1_cash_position,
        get_v1_cash_forecast,
        get_v1_cash_compliance,
        simulate_v1_cash,
    )

    pos = get_v1_cash_position()
    assert pos["ok"] is True
    assert pos["credit_facility_limit_nok"] == 150_000_000.0

    forecast = get_v1_cash_forecast()
    assert forecast["ok"] is True
    assert forecast["count"] == 30
    assert forecast["period"] == "2026-M11"

    comp = get_v1_cash_compliance()
    assert comp["ok"] is True
    assert comp["is_within_statutory_limit"] is True

    sim = simulate_v1_cash({
        "scenario_name": "API Test Scenario",
        "tax_revenue_delta_percent": -3.0,
        "state_grant_delay_days": 2,
    })
    assert sim["ok"] is True
    assert len(sim["sha256_audit_seal"]) == 64


def test_cash_runner_cli_execution():
    """Tester at tools/cash_management_runner.py kjører feilfritt via CLI."""
    cmd = [sys.executable, str(ROOT_DIR / "tools" / "cash_management_runner.py"), "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert "bank_balance_nok" in data
    assert data["credit_facility_limit_nok"] == 150000000.0
