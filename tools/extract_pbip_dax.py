#!/usr/bin/env python3
"""
Extracts all 101 DAX measures from pbi-rep-project-rapport TMDL
into powerbi/10_PBIP_Rapport_DAX_Measures.dax
"""

from collections import defaultdict
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
TMDL_FILE = BASE_DIR / "pbi-rep-project-rapport.SemanticModel" / "definition" / "tables" / "_Måltall.tmdl"
OUTPUT_DAX = BASE_DIR / "powerbi" / "10_PBIP_Rapport_DAX_Measures.dax"

def main():
    if not TMDL_FILE.exists():
        print(f"Error: {TMDL_FILE} not found")
        sys.exit(1)

    with open(TMDL_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Split measures block
    measure_blocks = re.split(r'\n\tmeasure\s+', text)
    blocks = measure_blocks[1:]

    measures_by_folder = defaultdict(list)

    for block in blocks:
        lines = block.splitlines()
        first_line = lines[0]
        m_name = first_line.split("=")[0].strip()
        
        folder = "Ukategorisert"
        fmt = ""
        formula_lines = []
        
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            stripped = line.strip()
            if stripped.startswith("column ") or stripped.startswith("partition "):
                break
            elif stripped.startswith("formatString:"):
                fmt = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("displayFolder:"):
                folder = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("lineageTag:"):
                pass
            elif stripped.startswith("annotation"):
                pass
            else:
                formula_lines.append(line)
            idx += 1
            
        full_formula = "\n".join(formula_lines)
        if "=" in full_formula:
            formula = full_formula.split("=", 1)[1].strip()
        else:
            formula = full_formula.strip()

        clean_formula_lines = []
        for fl in formula.splitlines():
            cleaned = re.sub(r'^\t{2,4}', '', fl)
            clean_formula_lines.append(cleaned)
        clean_formula = "\n".join(clean_formula_lines).strip()

        measures_by_folder[folder].append({
            "name": m_name,
            "formula": clean_formula,
            "format": fmt,
            "folder": folder
        })

    total_m = sum(len(v) for v in measures_by_folder.values())

    out_lines = [
        "// ==============================================================================",
        "// 🏛️ KRISTIANSAND KOMMUNE — OFFISIELT POWER BI RAPPORT DAX-BIBLIOTEK",
        "// ==============================================================================",
        "// Kilde: pbi-rep-project-rapport.pbip (TMDL _Måltall)",
        f"// Totalt: {total_m} DAX-måltall fordelt på {len(measures_by_folder)} mapper",
        "// Standard: Edward Tufte Data-Ink Ratio, KOSTRA og Kommuneloven § 14-5",
        "// ==============================================================================",
        ""
    ]

    for folder in sorted(measures_by_folder.keys()):
        m_list = measures_by_folder[folder]
        out_lines.append("// " + "-" * 78)
        out_lines.append(f"// MAPPE: {folder} ({len(m_list)} måltall)")
        out_lines.append("// " + "-" * 78)
        out_lines.append("")

        for m in m_list:
            name = m["name"]
            clean_name = name.replace('"', '').replace("'", "").strip()
            m_bracket = f"[{clean_name}]"

            out_lines.append(f"{m_bracket} =")
            out_lines.append(m["formula"])
            if m["format"]:
                out_lines.append(f"/* Format: {m['format']} | Mappe: {folder} */")
            else:
                out_lines.append(f"/* Mappe: {folder} */")
            out_lines.append("")

    OUTPUT_DAX.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DAX, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"✅ Skrevet til {OUTPUT_DAX} ({OUTPUT_DAX.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
