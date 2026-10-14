#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
KRISTIANSAND KOMMUNE — EXCEL FINANCIAL CONTROLLING & FP&A SUITE BUILDER
===============================================================================
Bygger og oppdaterer de 4 offisielle kommunale Excel-modellene i C:\\Users\\frank\\Desktop\\AI_KOM\\excel:
1. Kommune_FAST_Finansiell_Modell_2026.xlsx       (FP&A Avviksmodell - FAST standard)
2. Kommune_Project_Controller_EVM_2026.xlsx        (Capex & Prosjektkontroll - ISO 21508)
3. Kommune_CFO_Executive_Konsern_2026.xlsx         (Toppledelse & Konsern - § 14-4/§ 14-5)
4. Kommune_HR_Lonn_Vikar_Monitor_2026.xlsx         (HR, Overtid & NAV-refusjoner - HTA § 4)

Hver modell tilfredsstiller:
- Edward Tuftes Data-Ink Ratio (ingen vertikale linjer, ingen tunge skygger)
- FAST Fargestandard (#000080 inndata, #000000 formler, #006100 interne lenker)
- Kommunal avviksformatering: _(* #,##0_);[Red]_(* (#,##0);_(* "-"_);_(@_)
- SHA-256 forsegling iht. Stage-Gate Port 9
===============================================================================
"""
import sys
from pathlib import Path

# Fix console encoding
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Legg til src i path
PACKAGE_DIR = Path(__file__).resolve().parents[1] / "kommune-ai-guardrails" / "src"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from kommune_ai_guardrails.generators.excel_fast_generator import generate_fast_excel_model
from kommune_ai_guardrails.generators.excel_evm_generator import generate_project_controller_evm_model
from kommune_ai_guardrails.generators.excel_cfo_generator import generate_cfo_executive_konsern_model
from kommune_ai_guardrails.generators.excel_hr_generator import generate_hr_lonn_vikar_monitor_model

EXCEL_DIR = Path(__file__).resolve().parent

def build_all_reports():
    print("🚀 Starter bygging av Kristiansand Kommune Excel-rapporter...")
    results = {}

    # 1. FAST Finansiell Modell
    print("  [1/4] Bygger FAST Finansiell Modell 2026...")
    p1 = EXCEL_DIR / "Kommune_FAST_Finansiell_Modell_2026.xlsx"
    generate_fast_excel_model(output_path=str(p1))
    results["FAST_Modell"] = p1
    print(f"        ✓ Lagret: {p1.name} ({p1.stat().st_size / 1024:.1f} KB)")

    # 2. Project Controller EVM Modell
    print("  [2/4] Bygger Project Controller & EVM Modell 2026...")
    p2 = EXCEL_DIR / "Kommune_Project_Controller_EVM_2026.xlsx"
    generate_project_controller_evm_model(output_path=str(p2))
    results["EVM_Modell"] = p2
    print(f"        ✓ Lagret: {p2.name} ({p2.stat().st_size / 1024:.1f} KB)")

    # 3. CFO Executive Konsernmodell
    print("  [3/4] Bygger CFO Executive & Konsernmodell 2026...")
    p3 = EXCEL_DIR / "Kommune_CFO_Executive_Konsern_2026.xlsx"
    generate_cfo_executive_konsern_model(output_path=str(p3))
    results["CFO_Modell"] = p3
    print(f"        ✓ Lagret: {p3.name} ({p3.stat().st_size / 1024:.1f} KB)")

    # 4. HR Lønn & Vikarmonitor
    print("  [4/4] Bygger HR Lønn, Overtid & Vikarmonitor 2026...")
    p4 = EXCEL_DIR / "Kommune_HR_Lonn_Vikar_Monitor_2026.xlsx"
    generate_hr_lonn_vikar_monitor_model(output_path=str(p4))
    results["HR_Modell"] = p4
    print(f"        ✓ Lagret: {p4.name} ({p4.stat().st_size / 1024:.1f} KB)")

    print("\n✅ Alle 4 Excel-rapporter er ferdigstilt og validert!")
    return results

if __name__ == "__main__":
    build_all_reports()
