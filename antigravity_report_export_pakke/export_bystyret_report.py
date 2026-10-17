"""
Bystyret M10 Økonomirapport Generator
Kristiansand kommune — Control Office Hub
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.report_export_engine import BystyretReportGenerator, generate_bystyret_pptx

def generate_bystyre_presentation(output_pptx_path: str, data: dict):
    generator = BystyretReportGenerator(data=data)
    res = generator.generate(output_path=output_pptx_path)
    print(f"Presentation saved successfully to: {output_pptx_path}")
    return res

if __name__ == "__main__":
    test_data = {
        "kommune": "Kristiansand kommune",
        "periode": "M10 Oktober 2026",
        "netto_driftsresultat_pct": 1.25,
        "disposisjonsfond_pct": 4.35,
        "netto_lanegjeld_pct": 76.8,
        "signee": "Frank Ellingsen, Senior Financial Controller",
        "revisjon": "Telemark Revisjon IKS",
    }
    out = ROOT_DIR / "reports" / "Bystyret_M10_Okonomi_Rapport.pptx"
    generate_bystyre_presentation(str(out), test_data)
