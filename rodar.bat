@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title ChurnShield
color 0B

echo.
echo  ========================================
echo   ChurnShield
echo  ========================================
echo.

REM --- encontrar Python (funciona mesmo se PATH do Explorer for diferente) ---
set "PY="
python --version >nul 2>&1 && set "PY=python"
if not defined PY py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY py --version >nul 2>&1 && set "PY=py"

if not defined PY (
    echo  [ERRO] Python nao encontrado.
    echo.
    echo  Instale em: https://www.python.org/downloads/
    echo  Na instalacao, marque "Add python.exe to PATH".
    echo.
    echo  Detalhes salvos em rodar.log
    echo Python nao encontrado >> rodar.log
    pause
    exit /b 1
)

echo  Python: %PY%
echo  Pasta: %CD%
echo.

REM --- ambiente virtual ---
if not exist "venv\Scripts\python.exe" (
    echo  [1/3] Criando ambiente virtual...
    %PY% -m venv venv
    if errorlevel 1 (
        echo  [ERRO] Falha ao criar venv. Veja rodar.log
        echo Falha venv >> rodar.log
        pause
        exit /b 1
    )
    echo  [2/3] Instalando dependencias (pode demorar na 1a vez)...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip -q
    pip install -r requirements.txt
    if errorlevel 1 (
        echo  [ERRO] Falha no pip install. Veja rodar.log
        pause
        exit /b 1
    )
) else (
    call venv\Scripts\activate.bat
)

REM --- .env ---
if not exist .env (
    echo  [3/3] Criando .env...
    copy /Y .env.example .env >nul
) else (
    echo  [3/3] .env ok
)

echo.
echo  Abrindo navegador em http://localhost:8000
start "" http://localhost:8000

echo.
echo  Servidor rodando. NAO FECHE esta janela.
echo  Para parar: Ctrl+C ou feche esta janela.
echo.

venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
if errorlevel 1 (
    echo.
    echo  [ERRO] Servidor parou com erro.
    pause
)
