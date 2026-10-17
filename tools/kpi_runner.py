#!/usr/bin/env python3
"""
Kristiansand Kommune — Top 3 KPI & Budsjetthierarki CLI Runner
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

from app.services.top3_kpi_service import Top3KpiService


def format_nok(val: float) -> str:
    return f"{val:,.0f} kr".replace(",", " ")


def main():
    parser = argparse.ArgumentParser(
        description="Kristiansand Kommune — Top 3 Finansielle KPIs & Budsjetthierarki",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--json", action="store_true", help="Formatér respons som JSON")
    parser.add_argument("--sector", type=str, default=None, help="Filtrer på spesifikk sektor (f.eks. OMR-02)")
    args = parser.parse_args()

    svc = Top3KpiService()
    payload = svc.get_dashboard_payload()

    if args.json:
        if args.sector:
            sec = svc.get_sector(args.sector)
            print(json.dumps(sec.model_dump() if sec else {"error": "Sector not found"}, indent=2, ensure_ascii=False))
        else:
            print(payload.model_dump_json(indent=2))
        return

    print("\n" + "=" * 80)
    print(f"🏛️  {payload.kommune.upper()} — TOP 3 FINANSIELLE NØKKELTALL ({payload.periode})")
    print("=" * 80)

    for k, item in payload.top3_kpis.items():
        status_sym = "🟢" if item.status == "GRØNN" else ("🟡" if item.status == "GUL" else "🔴")
        print(f"  {status_sym} {item.navn.upper()}:")
        print(f"     Nåverdi:     {item.verdi:.2f} {item.enhet}")
        print(f"     Mål Kommune: {item.mål_kommune:.2f} {item.enhet}")
        print(f"     Mål TBU:     {item.mål_tbu:.2f} {item.enhet}")
        print("-" * 80)

    print("\n" + "=" * 80)
    print("📊 BUDSJETTHIERARKI & SEKTORAVVIK (YTD)")
    print("=" * 80)
    print(f"{'Sektor-ID':<10} {'Sektornavn':<32} {'Ramme (NOK)':>16} {'Forbruk (NOK)':>16} {'Avvik':>12} {'Status':<10}")
    print("-" * 102)

    for sec in payload.budsjetthierarki:
        status_sym = "🟢" if sec.triage_status == "GRØNN" else ("🟡" if sec.triage_status == "GUL" else "🔴")
        print(
            f"{sec.sektor_id:<10} "
            f"{sec.sektor_navn:<32} "
            f"{format_nok(sec.ramme_ytd_nok):>16} "
            f"{format_nok(sec.forbruk_ytd_nok):>16} "
            f"{format_nok(sec.avvik_ytd_nok):>12} "
            f"{status_sym + ' ' + sec.triage_status:<10}"
        )

    print("-" * 102)
    print(f"  Revisjonssegl: sha256: {payload.sha256_audit_seal}")
    print("=" * 102)


if __name__ == "__main__":
    main()
