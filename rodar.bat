@echo off
cd /d "%~dp0"
title ChurnShield

echo Iniciando ChurnShield...
start "" http://127.0.0.1:8000

venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

echo.
echo Servidor parou.
pause
