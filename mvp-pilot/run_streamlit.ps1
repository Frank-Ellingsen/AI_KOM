# PowerShell launcher for Kristiansand EPM MVP-Pilot
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Starter Kristiansand EPM MVP-Pilot Streamlit Web Portal..." -ForegroundColor Green
Write-Host "Enhet: Bo og Miljø (KOSTRA 254)" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan

Set-Location -Path $PSScriptRoot
python run_web.py
