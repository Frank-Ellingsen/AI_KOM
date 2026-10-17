#!/usr/bin/env python3
"""
Kristiansand Kommune — Automated Report Export CLI Runner (.pptx)
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

from app.services.report_export_engine import generate_bystyret_pptx


def main():
    parser = argparse.ArgumentParser(
        description="Kristiansand Kommune — Automated Bystyret Report Generator (.pptx)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--out", type=str, default=str(ROOT_DIR / "reports" / "Bystyret_M10_Okonomi_Rapport.pptx"), help="Sti til utgående .pptx fil")
    parser.add_argument("--json", action="store_true", help="Formatér respons som JSON")
    args = parser.parse_args()

    res = generate_bystyret_pptx(output_path=args.out)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print("\n" + "=" * 80)
    print("🏛️  KRISTIANSAND KOMMUNE — BYSTYRET RAPPORTEXPORT FULLFØRT")
    print("=" * 80)
    print(f"  Filbane:        {res['file_path']}")
    print(f"  Filnavn:        {res['file_name']}")
    print(f"  Antall slides:  {res['slides_count']} (16:9 widescreen layout)")
    print(f"  Filstørrelse:   {res['file_size_bytes']:,} bytes".replace(",", " "))
    print(f"  SHA-256 stempel:{res['sha256_audit_seal']}")
    print(f"  Generert:       {res['generated_at']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
