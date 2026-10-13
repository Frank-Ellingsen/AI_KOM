#!/usr/bin/env python3
"""
CLI-skript for å indeksere rådokumenter inn i Kommune AI Guardrails SQLite-databasen.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Legg til src i sys.path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kommune_ai_guardrails.ingest import ingest_all


def main() -> int:
    try:
        count = ingest_all()
        print(f"\n✅ Indeksering fullført med {count} chunks.")
        return 0
    except Exception as exc:
        print(f"\n❌ Feil under indeksering: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
