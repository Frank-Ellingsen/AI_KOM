#!/usr/bin/env python3
"""
Kristiansand Kommune — Cash Management & Likviditetsstyring CLI Runner
jf. Kommuneloven §§ 14-1, 14-13, 14-14, 14-15 og Finansforskriften.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Fix console encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.cash_engine import CashManagementEngine
from app.schemas.cash import CashSimulationScenario


def format_nok(val: float) -> str:
    return f"{val:,.0f} kr".replace(",", " ")


def print_tufte_header(title: str):
    print("\n" + "=" * 78)
    print(f"🏛️  KRISTIANSAND KOMMUNE — {title.upper()}")
    print("=" * 78)


def run_position(engine: CashManagementEngine, as_json: bool = False):
    pos = engine.get_current_position()
    if as_json:
        print(pos.model_dump_json(indent=2))
        return

    print_tufte_header("Konsernkonto & Kassakredittstatus (Nåbilde)")
    print(f"  Avstemmingsdato:            {pos.as_of_date}")
    print(f"  Innestående konsernkonto:   {format_nok(pos.bank_balance_nok):>20}")
    print(f"  Vedtatt driftskredittramme: {format_nok(pos.credit_facility_limit_nok):>20}  (Kommuneloven § 14-14)")
    print(f"  Benyttet kassakreditt:      {format_nok(pos.credit_facility_used_nok):>20}")
    print(f"  Disponibel likviditetsramme:{format_nok(pos.available_liquidity_nok):>20}")
    print(f"  Utnyttelsesgrad:            {pos.utilization_rate_percent:>19.1f} %")
    print(f"  Finansiell status:          {'🟢 ' + pos.status if pos.status == 'BALANCED' else '🟡 ' + pos.status}")
    print("-" * 78)


def run_forecast(engine: CashManagementEngine, as_json: bool = False):
    entries = engine.get_daily_forecast()
    if as_json:
        print(json.dumps([e.model_dump() for e in entries], indent=2, ensure_ascii=False))
        return

    print_tufte_header("30-Dagers Rullende Likviditetsprognose (M11 November 2026)")
    print(f"{'Dato':<11} {'Innbetalt':>14} {'Utbetalt':>14} {'Netto':>14} {'Sluttsaldo':>15} {'Status':<12}")
    print("-" * 84)

    for e in entries:
        inflow = e.inflow_tax_nok + e.inflow_state_grants_nok + e.inflow_other_nok
        outflow = e.outflow_payroll_nok + e.outflow_suppliers_nok + e.outflow_debt_service_nok
        status_symbol = "🟢 OK" if e.status == "OK" else ("🟡 KREDITT" if e.status == "UTILIZING_CREDIT" else "🔴 FARE")
        print(
            f"{e.entry_date:<11} "
            f"{format_nok(inflow):>14} "
            f"{format_nok(outflow):>14} "
            f"{format_nok(e.net_cash_flow_nok):>14} "
            f"{format_nok(e.projected_end_balance_nok):>15} "
            f"{status_symbol:<12}"
        )

    print("-" * 84)
    min_bal = min(e.projected_end_balance_nok for e in entries)
    max_draw = max(e.credit_draw_nok for e in entries)
    print(f"  Estimert laveste saldo:      {format_nok(min_bal)} (14. nov før rammetilskudd)")
    print(f"  Maksimalt kassakreditttrekk: {format_nok(max_draw)} (Vedtatt ramme: {format_nok(engine.credit_limit_nok)})")
    print("=" * 84)


def run_simulation(
    engine: CashManagementEngine,
    name: str,
    tax_delta: float,
    grant_delay: int,
    extra_expense: float,
    as_json: bool = False,
):
    sc = CashSimulationScenario(
        scenario_name=name,
        tax_revenue_delta_percent=tax_delta,
        state_grant_delay_days=grant_delay,
        extraordinary_expense_nok=extra_expense,
    )
    res = engine.simulate_scenario(sc)

    if as_json:
        print(res.model_dump_json(indent=2))
        return

    print_tufte_header(f"Scenariesimulering (What-If): {res.scenario_name}")
    print(f"  Parameter endring skatt:     {tax_delta:+.1f} %")
    print(f"  Forsinkelse rammetilskudd:   {grant_delay} dager")
    print(f"  Ekstraordinær kostnad:       {format_nok(extra_expense)}")
    print("-" * 78)
    print(f"  Opprinnelig laveste saldo:   {format_nok(res.baseline_min_balance_nok):>20}")
    print(f"  Simulert laveste saldo:      {format_nok(res.simulated_min_balance_nok):>20}")
    print(f"  Simulert toppkreditt-trekk:  {format_nok(res.simulated_max_credit_draw_nok):>20}")
    print(f"  Vedtatt ramme (§ 14-14):     {format_nok(res.credit_limit_nok):>20}")
    print(f"  Dager i driftskreditt:       {res.days_in_overdraft:>20} dager")
    print(f"  Estimert merrentekostnad:    {format_nok(res.estimated_interest_cost_delta_nok):>20}")
    print(f"  Rammebrudd / overtrekk:      {'🔴 JA (RAMMEBRUDD)' if res.overdraft_limit_breached else '🟢 NEI (INNENFOR RAMME)'}")
    print(f"  Samsvarsvurdering:           {res.compliance_status}")
    print(f"  Kryptografisk revisjonssegl: {res.sha256_audit_seal}")
    print("-" * 78)
    print(f"  Oppsummering: {res.summary_message}")
    print("=" * 78)


def run_compliance(engine: CashManagementEngine, as_json: bool = False):
    rep = engine.check_compliance()
    if as_json:
        print(rep.model_dump_json(indent=2))
        return

    print_tufte_header("Finansforskriften & Kommuneloven Kontrollrapport")
    print(f"  Kontrolldato:               {rep.as_of_date}")
    print(f"  Vedtatt kredittramme:       {format_nok(rep.credit_limit_authorized_nok)}")
    print(f"  Projisert maks trekk:       {format_nok(rep.max_projected_draw_nok)}")
    print(f"  Innenfor lovlig ramme:      {'🟢 JA' if rep.is_within_statutory_limit else '🔴 NEI'}")
    print(f"  Valutadenominering:         {rep.currency_denomination}")
    print(f"  Revisjonssegl (SHA-256):    {rep.sha256_audit_seal}")
    print("\n  Hjemmelsgrunnlag:")
    for b in rep.legal_basis:
        print(f"    * {b}")
    print("\n  Godkjente finansinstitusjoner (Finansreglementet):")
    for inst in rep.authorized_financial_institutions:
        print(f"    * {inst}")
    print("-" * 78)
    print(f"  Konklusjon: {rep.compliance_verdict}")
    print("=" * 78)


def main():
    parser = argparse.ArgumentParser(
        description="Kristiansand Kommune — Cash Management & Likviditetsstyring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--position", action="store_true", help="Vis nåværende konsernkonto- og kredittstatus")
    parser.add_argument("--forecast", action="store_true", help="Vis 30-dagers rullende likviditetsprognose")
    parser.add_argument("--simulate", action="store_true", help="Kjør What-If scenariesimulering")
    parser.add_argument("--compliance", action="store_true", help="Valider mot Kommuneloven § 14-14 og Finansforskriften")
    parser.add_argument("--scenario-name", default="Forsinket Skatt & Ekstrakostnad", help="Navn på scenario")
    parser.add_argument("--tax-delta", type=float, default=-5.0, help="Prosentvis endring i skatt")
    parser.add_argument("--grant-delay", type=int, default=5, help="Dagers forsinkelse på rammetilskudd")
    parser.add_argument("--extra-expense", type=float, default=2500000.0, help="Ekstraordinære utgifter i NOK")
    parser.add_argument("--credit-limit", type=float, default=150000000.0, help="Vedtatt kassakredittramme")
    parser.add_argument("--json", action="store_true", help="Returner respons som JSON")

    args = parser.parse_args()

    engine = CashManagementEngine(credit_limit_nok=args.credit_limit)

    if args.forecast:
        run_forecast(engine, as_json=args.json)
    elif args.simulate:
        run_simulation(
            engine,
            name=args.scenario_name,
            tax_delta=args.tax_delta,
            grant_delay=args.grant_delay,
            extra_expense=args.extra_expense,
            as_json=args.json,
        )
    elif args.compliance:
        run_compliance(engine, as_json=args.json)
    else:
        # Standard: Vis position og forecast
        run_position(engine, as_json=args.json)
        if not args.json:
            run_compliance(engine, as_json=False)


if __name__ == "__main__":
    main()
