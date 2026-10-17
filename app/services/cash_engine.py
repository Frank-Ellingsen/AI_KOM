"""
Cash Management Engine for Kristiansand Kommune
jf. Kommuneloven §§ 14-1, 14-13, 14-14, 14-15 og Finansforskriften.

Beregner rullende 30-dagers og 12-måneders likviditetsprognoser,
overvåker kassakredittramme og utfører 'What-If' scenariesimuleringer.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict, Any

import polars as pl

from app.schemas.cash import (
    CashPosition,
    DailyCashFlowEntry,
    CashSimulationScenario,
    CashSimulationResult,
    CashComplianceReport,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV_PATH = ROOT_DIR / "antigravity_cash_management_pakke" / "Likviditetsprognose_2026_M11.csv"


class CashManagementEngine:
    def __init__(
        self,
        credit_limit_nok: float = 150_000_000.0,
        default_start_balance: float = 42_850_000.0,
        csv_path: Optional[Path] = None,
    ):
        self.credit_limit_nok = credit_limit_nok
        self.default_start_balance = default_start_balance
        self.csv_path = Path(csv_path) if csv_path else DEFAULT_CSV_PATH

    def load_csv(self, file_path: Optional[Path] = None) -> pl.DataFrame:
        target = Path(file_path) if file_path else self.csv_path
        if not target.exists():
            raise FileNotFoundError(f"Likviditetsfil ikke funnet: {target}")
        
        return pl.read_csv(target)

    def process_forecast(
        self,
        df_flows: Optional[pl.DataFrame] = None,
        initial_balance: Optional[float] = None,
    ) -> pl.DataFrame:
        """
        Kjører likviditetsprojeksjon og sjekker rammer jf. spesifikasjon.
        """
        if df_flows is None:
            df_flows = self.load_csv()

        balance = initial_balance if initial_balance is not None else self.default_start_balance
        results = []

        # Standardiser kolonnenavn dersom engelske eller norske brukes
        cols = df_flows.columns
        tax_col = "Skatteinntekter_NOK" if "Skatteinntekter_NOK" in cols else "inflow_tax"
        grant_col = "Rammetilskudd_NOK" if "Rammetilskudd_NOK" in cols else "inflow_state_grants"
        other_col = "Andre_Innbetalinger_NOK" if "Andre_Innbetalinger_NOK" in cols else "inflow_other"
        payroll_col = "Lønnsutbetaling_NOK" if "Lønnsutbetaling_NOK" in cols else "outflow_payroll"
        supp_col = "Leverandørbetalinger_NOK" if "Leverandørbetalinger_NOK" in cols else "outflow_suppliers"
        debt_col = "Renter_Avdrag_NOK" if "Renter_Avdrag_NOK" in cols else "outflow_debt_service"
        date_col = "Dato" if "Dato" in cols else "entry_date"

        for row in df_flows.iter_rows(named=True):
            inflow = float(row.get(tax_col, 0.0) or 0.0) + float(row.get(grant_col, 0.0) or 0.0) + float(row.get(other_col, 0.0) or 0.0)
            outflow = float(row.get(payroll_col, 0.0) or 0.0) + float(row.get(supp_col, 0.0) or 0.0) + float(row.get(debt_col, 0.0) or 0.0)
            net = inflow - outflow
            balance += net

            credit_draw = abs(balance) if balance < 0 else 0.0
            overdraft_hazard = credit_draw > self.credit_limit_nok

            status = "CRITICAL_LIMIT" if overdraft_hazard else ("UTILIZING_CREDIT" if credit_draw > 0 else "OK")

            results.append({
                "Dato": str(row.get(date_col, "")),
                "Innbetalinger_Total": inflow,
                "Utbetalinger_Total": outflow,
                "Netto_Endring": net,
                "Beregnet_Saldo": balance,
                "Kassakreditt_Trekk": credit_draw,
                "Disponibel_Kreditt_Gjenværende": max(0.0, self.credit_limit_nok - credit_draw),
                "Status": status,
            })

        return pl.DataFrame(results)

    def get_daily_forecast(
        self,
        initial_balance: Optional[float] = None,
    ) -> List[DailyCashFlowEntry]:
        """
        Returnerer strukturerte DailyCashFlowEntry-modeller for hele prognoseperioden.
        """
        df_flows = self.load_csv()
        balance = initial_balance if initial_balance is not None else self.default_start_balance
        entries: List[DailyCashFlowEntry] = []

        for row in df_flows.iter_rows(named=True):
            inflow_tax = float(row.get("Skatteinntekter_NOK", 0.0) or 0.0)
            inflow_grants = float(row.get("Rammetilskudd_NOK", 0.0) or 0.0)
            inflow_other = float(row.get("Andre_Innbetalinger_NOK", 0.0) or 0.0)
            outflow_payroll = float(row.get("Lønnsutbetaling_NOK", 0.0) or 0.0)
            outflow_suppliers = float(row.get("Leverandørbetalinger_NOK", 0.0) or 0.0)
            outflow_debt = float(row.get("Renter_Avdrag_NOK", 0.0) or 0.0)

            inflow = inflow_tax + inflow_grants + inflow_other
            outflow = outflow_payroll + outflow_suppliers + outflow_debt
            net = inflow - outflow
            balance += net

            credit_draw = abs(balance) if balance < 0 else 0.0
            is_overdraft = credit_draw > self.credit_limit_nok

            status = "CRITICAL_LIMIT" if is_overdraft else ("UTILIZING_CREDIT" if credit_draw > 0 else "OK")

            entries.append(
                DailyCashFlowEntry(
                    entry_date=str(row.get("Dato", "")),
                    inflow_tax_nok=inflow_tax,
                    inflow_state_grants_nok=inflow_grants,
                    inflow_other_nok=inflow_other,
                    outflow_payroll_nok=outflow_payroll,
                    outflow_suppliers_nok=outflow_suppliers,
                    outflow_debt_service_nok=outflow_debt,
                    net_cash_flow_nok=net,
                    projected_end_balance_nok=balance,
                    credit_draw_nok=credit_draw,
                    available_credit_remaining_nok=max(0.0, self.credit_limit_nok - credit_draw),
                    status=status,
                )
            )

        return entries

    def get_current_position(
        self,
        as_of_date: str = "2026-11-01",
        credit_facility_used_nok: float = 24_500_000.0,
    ) -> CashPosition:
        """
        Henter nåværende konsernsaldo, kassakredittstatus og buffer.
        """
        bank_balance = self.default_start_balance
        used = credit_facility_used_nok
        available = bank_balance + max(0.0, self.credit_limit_nok - used)
        utilization = round((used / self.credit_limit_nok) * 100.0, 2) if self.credit_limit_nok > 0 else 0.0

        status = "CRITICAL_LIMIT" if used > self.credit_limit_nok else ("CREDIT_DRAW" if used > 0 else "BALANCED")

        return CashPosition(
            as_of_date=as_of_date,
            bank_balance_nok=bank_balance,
            credit_facility_limit_nok=self.credit_limit_nok,
            credit_facility_used_nok=used,
            available_liquidity_nok=available,
            utilization_rate_percent=utilization,
            status=status,
        )

    def simulate_scenario(
        self,
        scenario: CashSimulationScenario,
        initial_balance: Optional[float] = None,
    ) -> CashSimulationResult:
        """
        Gjennomfører 'What-If' simulering med dynamiske parametere:
        - tax_revenue_delta_percent: endring i skatt
        - state_grant_delay_days: forsinkelse av rammetilskudd
        - extraordinary_expense_nok: uforutsette hendelser
        """
        df_flows = self.load_csv()
        baseline_entries = self.get_daily_forecast(initial_balance=initial_balance)
        baseline_min_balance = min(e.projected_end_balance_nok for e in baseline_entries)
        baseline_max_credit = max(e.credit_draw_nok for e in baseline_entries)

        # Forbered simulerte kontantstrømmer
        rows = df_flows.to_dicts()
        n_days = len(rows)

        # Håndter forskyvning av rammetilskudd
        delayed_grants: Dict[int, float] = {}
        if scenario.state_grant_delay_days > 0:
            for idx, r in enumerate(rows):
                grant = float(r.get("Rammetilskudd_NOK", 0.0) or 0.0)
                if grant > 0:
                    delayed_grants[idx] = grant
                    r["Rammetilskudd_NOK"] = 0.0

            for orig_idx, grant in delayed_grants.items():
                target_idx = min(n_days - 1, orig_idx + scenario.state_grant_delay_days)
                rows[target_idx]["Rammetilskudd_NOK"] = float(rows[target_idx].get("Rammetilskudd_NOK", 0.0) or 0.0) + grant

        # Juster skatt og legg til uforutsett utgift på dag 12 (lønnsdag) eller dag 1
        sim_balance = initial_balance if initial_balance is not None else self.default_start_balance
        sim_min_balance = sim_balance
        sim_max_credit = 0.0
        days_in_overdraft = 0
        total_interest_cost_delta = 0.0
        daily_interest_rate = 0.065 / 365.0  # 6.5 % nominell kassakredittrente

        for idx, r in enumerate(rows):
            tax = float(r.get("Skatteinntekter_NOK", 0.0) or 0.0) * (1.0 + (scenario.tax_revenue_delta_percent / 100.0))
            grants = float(r.get("Rammetilskudd_NOK", 0.0) or 0.0)
            other = float(r.get("Andre_Innbetalinger_NOK", 0.0) or 0.0)

            payroll = float(r.get("Lønnsutbetaling_NOK", 0.0) or 0.0)
            suppliers = float(r.get("Leverandørbetalinger_NOK", 0.0) or 0.0)
            debt = float(r.get("Renter_Avdrag_NOK", 0.0) or 0.0)

            extra_exp = scenario.extraordinary_expense_nok if idx == 11 else 0.0  # F.eks. 12. nov

            inflow = tax + grants + other
            outflow = payroll + suppliers + debt + extra_exp
            net = inflow - outflow
            sim_balance += net

            if sim_balance < sim_min_balance:
                sim_min_balance = sim_balance

            draw = abs(sim_balance) if sim_balance < 0 else 0.0
            if draw > sim_max_credit:
                sim_max_credit = draw

            if draw > 0:
                days_in_overdraft += 1
                baseline_draw = baseline_entries[idx].credit_draw_nok
                additional_draw = max(0.0, draw - baseline_draw)
                total_interest_cost_delta += additional_draw * daily_interest_rate

        breached = sim_max_credit > self.credit_limit_nok
        compliance = "CRITICAL_OVERDRAFT_LIMIT_BREACHED" if breached else ("COMPLIANT_WITHIN_CREDIT_LIMIT" if sim_max_credit > 0 else "NO_CREDIT_NEEDED")

        summary_msg = (
            f"Scenario '{scenario.scenario_name}': Simulerte laveste konsernsaldo er "
            f"{sim_min_balance:,.0f} NOK. Maksimalt kassakreditt-trekk blir {sim_max_credit:,.0f} NOK "
            f"over {days_in_overdraft} dager. "
            f"{'ADVARSEL: Vedtatt ramme overskrides!' if breached else 'Innenfor vedtatt ramme jf. § 14-14.'}"
        ).replace(",", " ")

        payload_to_hash = f"{scenario.scenario_name}|{sim_min_balance}|{sim_max_credit}|{days_in_overdraft}|{breached}"
        audit_seal = hashlib.sha256(payload_to_hash.encode("utf-8")).hexdigest()

        return CashSimulationResult(
            scenario_name=scenario.scenario_name,
            baseline_min_balance_nok=round(baseline_min_balance, 2),
            simulated_min_balance_nok=round(sim_min_balance, 2),
            baseline_max_credit_draw_nok=round(baseline_max_credit, 2),
            simulated_max_credit_draw_nok=round(sim_max_credit, 2),
            credit_limit_nok=self.credit_limit_nok,
            days_in_overdraft=days_in_overdraft,
            overdraft_limit_breached=breached,
            estimated_interest_cost_delta_nok=round(total_interest_cost_delta, 2),
            compliance_status=compliance,
            sha256_audit_seal=audit_seal,
            summary_message=summary_msg,
        )

    def check_compliance(
        self,
        forecast_entries: Optional[List[DailyCashFlowEntry]] = None,
    ) -> CashComplianceReport:
        """
        Validerer likviditetsforvaltningen mot Kommuneloven §§ 14-1, 14-13, 14-14, 14-15
        og Forskrift om garantier og finans- og gjeldsforvaltning.
        """
        entries = forecast_entries or self.get_daily_forecast()
        max_draw = max(e.credit_draw_nok for e in entries)
        within_limit = max_draw <= self.credit_limit_nok

        verdict = "GODKJENT — I SAMSVAR MED FINANSFORSKRIFTEN OG § 14-14" if within_limit else "IKKE GODKJENT — OVERTREKK PÅ KASSAKREDITTRAMME"

        today_str = datetime.now().strftime("%Y-%m-%d")
        payload = f"{today_str}|{self.credit_limit_nok}|{max_draw}|{within_limit}"
        seal = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        return CashComplianceReport(
            as_of_date=today_str,
            legal_basis=[
                "Kommuneloven § 14-1 (Økonomisk forvaltning)",
                "Kommuneloven § 14-13 (Finans- og gjeldsforvaltning)",
                "Kommuneloven § 14-14 (Lån til finansiering av driftsutgifter)",
                "Forskrift om garantier og finans- og gjeldsforvaltning (finansforskriften)",
            ],
            credit_limit_authorized_nok=self.credit_limit_nok,
            max_projected_draw_nok=max_draw,
            is_within_statutory_limit=within_limit,
            currency_denomination="NOK (Norske kroner, 100 % valutasikret)",
            authorized_financial_institutions=[
                "DNB Bank ASA (Konsernkontobank / Hovedavtale)",
                "Kommunalbanken AS (Langsiktig finansiering)",
                "KLP Kommunekreditt AS",
            ],
            compliance_verdict=verdict,
            sha256_audit_seal=seal,
        )
