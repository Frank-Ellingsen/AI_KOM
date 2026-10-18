#!/usr/bin/env python3
"""
🏛️ Kristiansand Kommune — DuckDB Analytical Engine & OLAP Runner (Agent 14/Controller)
======================================================================================
Kjører høyhastighets in-memory OLAP-analyser, EVM-beregninger (CPI, EAC) og rotårsaks-
dekomponering over den kanoniske Star Schema-datamodellen.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

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

from app.services.duckdb_engine import DuckDbAnalyticalEngine


def format_nok(val: float) -> str:
    return f"{val:,.0f} kr".replace(",", " ")


def main():
    parser = argparse.ArgumentParser(
        description="Kristiansand Kommune — DuckDB In-Memory OLAP & EVM Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--summary", action="store_true", help="Vis samlet EVM-oppsummering for alle 6 virksomhetsområder")
    parser.add_argument("--sector", type=str, default=None, help="Filtrer på spesifikt virksomhetsområde")
    parser.add_argument("--unit", type=str, default=None, help="Vis enhetsdrilldown for spesifikk enhet eller sektor")
    parser.add_argument("--drivers", action="store_true", help="Vis topp 10 kontoarter med størst avvik")
    parser.add_argument("--query", type=str, default=None, help="Kjør vilkårlig analytisk DuckDB SQL-spørring")
    parser.add_argument("--year", type=int, default=2026, help="Regnskapsår (standard: 2026)")
    parser.add_argument("--month", type=int, default=9, help="Måned YTD (standard: 9)")
    parser.add_argument("--json", action="store_true", help="Formatér respons som JSON")
    args = parser.parse_args()

    engine = DuckDbAnalyticalEngine()

    # 1. Tilpasset SQL-spørring
    if args.query:
        df = engine.run_query(args.query)
        if args.json:
            print(df.to_json(orient="records", indent=2, force_ascii=False))
        else:
            print(df.to_string(index=False))
        return

    # 2. Kostnadsdrivere (Art)
    if args.drivers:
        drivers = engine.get_art_cost_drivers(ansvar_kode=args.unit, year=args.year)
        if args.json:
            print(json.dumps(drivers, indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 90)
            print(f"📊 TOPP 10 KOSTNADSDRIVERE (ART) — {args.year}-M{args.month:02d} YTD")
            print("=" * 90)
            print(f"{'Art':<6} {'Artsnavn':<35} {'Budsjett (NOK)':>16} {'Regnskap (NOK)':>16} {'Avvik (NOK)':>16}")
            print("-" * 90)
            for d in drivers:
                print(f"{d['art_kode']:<6} {d['art_navn'][:33]:<35} {format_nok(d['budsjett_ytd']):>16} {format_nok(d['regnskap_ytd']):>16} {format_nok(d['avvik_nok']):>16}")
            print("=" * 90)
        return

    # 3. Enhetsdrilldown
    if args.unit or args.sector:
        units = engine.get_unit_drilldown(sektor_navn=args.sector, year=args.year, month=args.month)
        if args.json:
            print(json.dumps(units, indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 95)
            print(f"🏢 ENHETSDRILLDOWN & AVVIK — {args.year}-M{args.month:02d} YTD")
            print("=" * 95)
            print(f"{'Ansvar':<18} {'Enhetsnavn':<30} {'Ramme (PV)':>15} {'Forbruk (AC)':>15} {'Avvik (CV)':>13} {'Status':<6}")
            print("-" * 95)
            for u in units:
                st_sym = "🔴" if u["status"] == "RØD" else ("🟡" if u["status"] == "GUL" else "🟢")
                print(f"{u['ansvar_kode']:<18} {u['enhet_navn'][:28]:<30} {format_nok(u['pv_nok']):>15} {format_nok(u['ac_nok']):>15} {format_nok(u['cv_nok']):>13} {st_sym} {u['status']}")
            print("=" * 95)
        return

    # 4. Standard: Sektoroppsummering (EVM)
    summary = engine.get_sector_evm_summary(year=args.year, month=args.month)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    print("\n" + "=" * 105)
    print(f"🏛️ KRISTIANSAND KOMMUNE — DUCKDB OLAP & EVM PERFORMANCE ({args.year}-M{args.month:02d} YTD)")
    print("=" * 105)
    print(f"{'Virksomhetsområde':<34} {'Ramme (PV)':>15} {'Forbruk (AC)':>15} {'Avvik (CV)':>13} {'CPI':>7} {'EAC Prognose':>16} {'Status':<6}")
    print("-" * 105)

    tot_pv = sum(s["pv_nok"] for s in summary)
    tot_ac = sum(s["ac_nok"] for s in summary)
    tot_cv = sum(s["cv_nok"] for s in summary)
    tot_eac = sum(s["eac_prognose"] for s in summary)
    tot_cpi = tot_pv / tot_ac if tot_ac > 0 else 1.0

    for s in summary:
        st_sym = "🔴" if s["triage_status"] == "RØD" else ("🟡" if s["triage_status"] == "GUL" else "🟢")
        print(
            f"{s['sektor_navn']:<34} "
            f"{format_nok(s['pv_nok']):>15} "
            f"{format_nok(s['ac_nok']):>15} "
            f"{format_nok(s['cv_nok']):>13} "
            f"{s['cpi']:>7.3f} "
            f"{format_nok(s['eac_prognose']):>16} "
            f"{st_sym} {s['triage_status']}"
        )

    print("-" * 105)
    tot_sym = "🟡" if tot_cv < -10000000 else "🟢"
    print(
        f"{'TOTALT KONSERN':<34} "
        f"{format_nok(tot_pv):>15} "
        f"{format_nok(tot_ac):>15} "
        f"{format_nok(tot_cv):>13} "
        f"{tot_cpi:>7.3f} "
        f"{format_nok(tot_eac):>16} "
        f"{tot_sym} KONSERN"
    )
    print("=" * 105)


if __name__ == "__main__":
    main()
