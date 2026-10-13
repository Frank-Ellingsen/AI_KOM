#!/usr/bin/env python3
"""
MVP Pilot Configuration - Kristiansand EPM & AI Kommunal Økonomistyring
"""

from pathlib import Path

# Prosjektstier
PILOT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PILOT_DIR.parent

# Excel-filreferanser
if (PILOT_DIR / "Mini_case_AI_kommunal_okonomistyring.xlsx").exists():
    EXCEL_SOURCE = PILOT_DIR / "Mini_case_AI_kommunal_okonomistyring.xlsx"
else:
    EXCEL_SOURCE = PROJECT_ROOT / "Mini_case_AI_kommunal_okonomistyring.xlsx"
EXCEL_OUTPUT = PILOT_DIR / "Mini_case_AI_kommunal_okonomistyring_oppdatert.xlsx"
EXCEL_RAPPORT_BO_MILJO = PILOT_DIR / "Rapport Enhet Bo og Miljø.xlsx"

# Databaser (lokal SQLite & DuckDB)
DB_SQLITE = PILOT_DIR / "mvp_pilot.db"
DB_DUCKDB = PILOT_DIR / "mvp_pilot.duckdb"

# Rapportmappe
REPORTS_DIR = PILOT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Ollama konfigurasjon
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "llama3.1:latest"
FALLBACK_OLLAMA_MODEL = "qwen2.5-coder-7b-32k:latest"

# Standard bruker og enhet for piloten
DEFAULT_ENHET = "5200"
DEFAULT_ENHET_NAVN = "Kommunal Boenhet (Bo og Miljø)"
DEFAULT_KOSTRA_FUNKSJON = "254"
DEFAULT_SAKSBEHANDLER = "Frank Ellingsen"
