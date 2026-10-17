"""
Test Suite for Automated Report Export Engine (.pptx / Bystyret)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from pptx import Presentation

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.report_export_engine import BystyretReportGenerator, generate_bystyret_pptx


def test_bystyret_report_generator_generates_valid_pptx(tmp_path):
    """Tester at BystyretReportGenerator produserer et gyldig 16:9 PowerPoint-dekk."""
    test_out = tmp_path / "test_bystyret_rapport.pptx"
    res = generate_bystyret_pptx(output_path=test_out)

    assert res["ok"] is True
    assert test_out.exists()
    assert test_out.stat().st_size > 5000
    assert len(res["sha256_audit_seal"]) == 64
    assert res["slides_count"] == 4

    # Inspiser PPTX-strukturen med python-pptx
    prs = Presentation(str(test_out))
    assert len(prs.slides) == 4

    # 16:9 bredskjerm (13.333 x 7.5 tommer)
    assert round(prs.slide_width.inches, 2) == 13.33
    assert round(prs.slide_height.inches, 2) == 7.5


def test_hub_api_server_export_pptx(tmp_path):
    """Tester at hub_api_server genererer PPTX via API."""
    from tools.hub_api_server import export_v1_bystyret_pptx

    res = export_v1_bystyret_pptx()
    assert res["ok"] is True
    assert res["slides_count"] == 4
    assert Path(res["file_path"]).exists()


def test_report_export_runner_cli():
    """Tester at tools/report_export_runner.py eksekverer feilfritt via CLI."""
    cmd = [sys.executable, str(ROOT_DIR / "tools" / "report_export_runner.py"), "--json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT_DIR))
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["ok"] is True
    assert data["slides_count"] == 4
