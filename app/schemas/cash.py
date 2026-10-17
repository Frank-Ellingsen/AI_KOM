"""
Pydantic schemas for Cash Management & Liquidity Forecasting
jf. Kommuneloven §§ 14-1, 14-13, 14-14, 14-15 og Finansforskriften.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class CashPosition(BaseModel):
    as_of_date: str = Field(..., description="Dato for saldoavstemming (YYYY-MM-DD)")
    bank_balance_nok: float = Field(..., description="Innestående på kommunens konsernkonto")
    credit_facility_limit_nok: float = Field(..., description="Vedtatt ramme for driftskreditt/kassakreditt jf. § 14-14")
    credit_facility_used_nok: float = Field(..., description="Benyttet driftskreditt per i dag")
    available_liquidity_nok: float = Field(..., description="Total disponibel likviditet (Bank + Unytta kreditt)")
    utilization_rate_percent: float = Field(..., description="Utnyttelsesgrad av kassakredittrammen i prosent")
    status: str = Field("BALANCED", description="Likviditetsstatus (BALANCED, CREDIT_DRAW, CRITICAL_LIMIT)")


class DailyCashFlowEntry(BaseModel):
    entry_date: str = Field(..., description="Dato (YYYY-MM-DD)")
    inflow_tax_nok: float = Field(0.0, description="Skatteinntekter (forskuddstrekk/skatteoppgjør)")
    inflow_state_grants_nok: float = Field(0.0, description="Statlige rammetilskudd og overføringer")
    inflow_other_nok: float = Field(0.0, description="Andre innbetalinger, gebyrer og MVA-kompensasjon")
    outflow_payroll_nok: float = Field(0.0, description="Lønnsutbetaling (Art 1010/1020)")
    outflow_suppliers_nok: float = Field(0.0, description="Leverandørbetalinger (Art 1100-1290)")
    outflow_debt_service_nok: float = Field(0.0, description="Renter og avdrag på lånegjeld (Art 1500)")
    net_cash_flow_nok: float = Field(..., description="Netto kontantstrøm for dagen")
    projected_end_balance_nok: float = Field(..., description="Beregnet sluttsaldo på konsernkonto")
    credit_draw_nok: float = Field(0.0, description="Trekk på kassakreditt ved negativ saldo")
    available_credit_remaining_nok: float = Field(..., description="Gjenværende disponibel kassakredittramme")
    status: str = Field("OK", description="Statuskode: OK, UTILIZING_CREDIT, CRITICAL_LIMIT")


class CashSimulationScenario(BaseModel):
    scenario_name: str = Field(..., description="Navn på simuleringsscenario")
    tax_revenue_delta_percent: float = Field(0.0, description="Prosentvis endring i skatteinngang (-20.0 til +20.0)")
    state_grant_delay_days: int = Field(0, description="Dagers forsinkelse på statlig rammetilskudd")
    extraordinary_expense_nok: float = Field(0.0, description="Ekstraordinære utgifter (f.eks. snøbrøyting, flom)")
    expense_account_art: int = Field(1270, description="Utgiftskonto / art (standard 1270 Andre tjenester)")


class CashSimulationResult(BaseModel):
    scenario_name: str
    baseline_min_balance_nok: float
    simulated_min_balance_nok: float
    baseline_max_credit_draw_nok: float
    simulated_max_credit_draw_nok: float
    credit_limit_nok: float
    days_in_overdraft: int
    overdraft_limit_breached: bool
    estimated_interest_cost_delta_nok: float
    compliance_status: str
    sha256_audit_seal: str
    summary_message: str


class CashComplianceReport(BaseModel):
    as_of_date: str
    legal_basis: List[str]
    credit_limit_authorized_nok: float
    max_projected_draw_nok: float
    is_within_statutory_limit: bool
    currency_denomination: str
    authorized_financial_institutions: List[str]
    compliance_verdict: str
    sha256_audit_seal: str
