@echo off
chcp 65001 >nul
title Kristiansand Kommune -- Oppdatering av Vektordatabase

echo =====================================================================
echo 🏛️  KRISTIANSAND KOMMUNE -- OPPDATERING AV VEKTORDATABASE
echo     Kommune AI Guardrails RAG ^& sqlite-vec
echo =====================================================================
echo.
echo [1/2] Sjekker rådokumenter i data\raw...
set "APP_DIR=%~dp0kommune-ai-guardrails"
set "PYTHON_EXE=C:\Users\frank\AppData\Local\Python\bin\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [2/2] Kjører indeksering med SentenceTransformer og sqlite-vec...
echo.
cd /d "%APP_DIR%"
"%PYTHON_EXE%" ingest.py

echo.
echo =====================================================================
echo Ferdig! Vektordatabasen er oppdatert.
echo =====================================================================
pause
