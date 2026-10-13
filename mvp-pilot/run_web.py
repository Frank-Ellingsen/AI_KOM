#!/usr/bin/env python3
"""
Dedicated Streamlit Web Launcher for MVP-Pilot
Kristiansand EPM · AI i Kommunal Økonomistyring (Bo og Miljø)

Usage:
    python run_web.py
    python run_web.py --port 8502
"""

import sys
import os
import shutil
import subprocess
import argparse
import urllib.request
import json
from pathlib import Path

PILOT_DIR = Path(__file__).resolve().parent
APP_SCRIPT = PILOT_DIR / "app_ui.py"

def check_ollama(base_url: str = "http://localhost:11434") -> bool:
    """Sjekker om Ollama kjører lokalt."""
    try:
        req = urllib.request.Request(f"{base_url}/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode())
            models = [m.get("name") for m in data.get("models", [])]
            print(f"[AI] Ollama er aktiv! Tilgjengelige modeller: {', '.join(models[:4])}")
            return True
    except Exception:
        print("[AI] Merk: Ollama svarer ikke på http://localhost:11434 (kjører med regelmotor-fallback).")
        return False

def main():
    parser = argparse.ArgumentParser(description="Start MVP-Pilot Streamlit Web Portal")
    parser.add_argument("--port", type=int, default=8501, help="Port for Streamlit (standard: 8501)")
    parser.add_argument("--headless", action="store_true", help="Kjør uten å åpne nettleser automatisk")
    args = parser.parse_args()

    print("=" * 70)
    print("KRISTIANSAND EPM · MVP-PILOT WEB PORTAL")
    print("AI-Assistert Økonomistyring: Bo og Miljø (funksjon 254)")
    print("=" * 70)

    # 1. Sjekk at app_ui.py finnes
    if not APP_SCRIPT.exists():
        print(f"[FEIL] Fant ikke {APP_SCRIPT}")
        sys.exit(1)

    # 2. Sjekk Ollama
    check_ollama()

    # 3. Start via python -m streamlit for maksimal robusthet på Windows
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(APP_SCRIPT),
        "--server.port", str(args.port),
        "--browser.gatherUsageStats", "false"
    ]

    if args.headless:
        cmd.extend(["--server.headless", "true"])

    print(f"\n[START] Åpner Streamlit på http://localhost:{args.port}...")
    print("[INFO] Trykk Ctrl+C i terminalen for å avslutte serveren.\n")

    try:
        subprocess.run(cmd, cwd=str(PILOT_DIR), check=True)
    except KeyboardInterrupt:
        print("\n[STOPP] Streamlit serveren ble avsluttet.")
    except Exception as e:
        print(f"[FEIL] Kunne ikke starte Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
