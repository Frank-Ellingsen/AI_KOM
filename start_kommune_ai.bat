@echo off
chcp 65001 >nul
title Kristiansand Kommune AI Assistent -- Oppstart

echo =====================================================================
echo 🏛️  KRISTIANSAND KOMMUNE -- AI OG REGELVERKSASSISTENT
echo     Økonomi og Virksomhetsstyring
echo =====================================================================
echo.
echo [1/3] Sjekker Python-miljø...

set "PYTHON_EXE=C:\Users\frank\AppData\Local\Python\bin\python.exe"
set "ROOT_DIR=%~dp0"
set "APP_DIR=%~dp0kommune-ai-guardrails"

if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [2/3] Starter Hub API & Vektor-DB tjeneste på http://127.0.0.1:8766...
start /b "" "%PYTHON_EXE%" "%ROOT_DIR%tools\hub_api_server.py"

echo [3/3] Starter Control Office Hub på http://localhost:8501...
cd /d "%APP_DIR%"
start "" "http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run app/app.py --server.port 8501 --server.headless false

pause
