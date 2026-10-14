#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
KRISTIANSAND KOMMUNE — POWER BI PBIP GENERATOR MODULE
===============================================================================
Bygger og validerer Power BI Developer Mode (.pbip) prosjektet:
- TMDL Semantisk Modell med Stjerneschema og VertiPaq-optimaliserte DAX-mål
- 7 PBIR rapportsider iht. Financial Times Visual Storytelling og Edward Tufte:
  1. Toppledelse (CFO Panel)
  2. Sektor Oppvekst & Grunnskole (Enhet 202)
  3. Sektor Helse & Mestring (Enhet 2540)
  4. Lønn, Overtid & Vikarmonitor
  5. Prognose & What-If Scenarier
  6. Investering & Prosjektkontroll (EVM)
  7. Revisjon & Audit Trail (Stage-Gate Port 9)
===============================================================================
"""

import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

def get_default_paths():
    base_dir = Path(__file__).resolve().parents[4] / "powerbi"
    data_root = Path(__file__).resolve().parents[4] / "erp_data"
    return base_dir, data_root

def build_pbip_project(target_dir: Path | None = None, data_dir: Path | None = None) -> Dict[str, Any]:
    """
    Bygger hele pbi_reporting_project.pbip i målkatalogen.
    """
    if target_dir is None or data_dir is None:
        def_base, def_data = get_default_paths()
        target_dir = target_dir or def_base
        data_dir = data_dir or def_data

    # Importerer og kjører fra build_pbi_reporting_project
    import importlib.util
    builder_script = target_dir / "build_pbi_reporting_project.py"
    if not builder_script.exists():
        raise FileNotFoundError(f"Fant ikke build skript: {builder_script}")

    spec = importlib.util.spec_from_file_location("build_pbi_reporting_project", str(builder_script))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Kjører byggingen
    module.setup_directories()
    module.build_semantic_model()
    module.build_report_pages()

    # Validerer resultatet
    rep_def = target_dir / "pbi_reporting_project.Report" / "definition"
    pages_json = json.loads((rep_def / "pages" / "pages.json").read_text(encoding="utf-8"))
    
    total_visuals = 0
    pages_info = []
    for p_id in pages_json["pageOrder"]:
        p_dir = rep_def / "pages" / p_id
        p_meta = json.loads((p_dir / "page.json").read_text(encoding="utf-8"))
        vis_count = len(list((p_dir / "visuals").iterdir()))
        total_visuals += vis_count
        pages_info.append({
            "id": p_id,
            "displayName": p_meta.get("displayName", p_id),
            "visualCount": vis_count
        })

    sem_def = target_dir / "pbi_reporting_project.SemanticModel" / "definition"
    tables = [t.stem for t in (sem_def / "tables").glob("*.tmdl")]

    return {
        "status": "SUCCESS",
        "pbip_file": str(target_dir / "pbi_reporting_project.pbip"),
        "pages_count": len(pages_info),
        "visuals_count": total_visuals,
        "tables_count": len(tables),
        "tables": tables,
        "pages": pages_info
    }

if __name__ == "__main__":
    res = build_pbip_project()
    print(f"Bygget PBIP prosjekt med {res['pages_count']} sider og {res['visuals_count']} visuals.")
