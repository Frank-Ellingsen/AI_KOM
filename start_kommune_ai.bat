@echo off
chcp 65001 >nul
title Kristiansand Kommune AI Assistent -- Oppstart

echo =====================================================================
echo 🏛️  KRISTIANSAND KOMMUNE -- AI OG REGELVERKSASSISTENT
echo     Økonomi og Virksomhetsstyring
echo =====================================================================
echo.
echo [1/2] Sjekker Python og Streamlit-miljø...

set "PYTHON_EXE=C:\Users\frank\AppData\Local\Python\bin\python.exe"
set "APP_DIR=C:\Users\frank\Desktop\AI_KOM\kommune-ai-guardrails"

if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [2/2] Starter Control Office Hub på http://localhost:8501...
cd /d "%APP_DIR%"
start "" "http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run app/app.py --server.port 8501 --server.headless false

pause
