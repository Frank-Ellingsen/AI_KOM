#!/usr/bin/env python3
"""
Eksempel på L3-eksekverbart skript.
Koden i scripts/ kjøres direkte i terminalen og bruker 0 kode-tokens i agentens kontekstvindu.
"""

import sys
import json

def process_data(input_val: str):
    return {
        "status": "success",
        "processed_value": input_val.upper(),
        "message": "Processed efficiently without context bloat."
    }

if __name__ == "__main__":
    val = sys.argv[1] if len(sys.argv) > 1 else "default_input"
    res = process_data(val)
    print(json.dumps(res, indent=2))
