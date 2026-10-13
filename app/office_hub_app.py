#!/usr/bin/env python3
"""
Kristiansand Kommune — Control Office Hub Streamlit App
Entry-point i henhold til OFFICE_DASHBOARD_HUB_SPEC.md.
Delegerer til app/app.py i kommune-ai-guardrails.
"""

from pathlib import Path
import sys

APP_DIR = Path(__file__).resolve().parent.parent / "kommune-ai-guardrails" / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Start app.py
import app
