@echo off
cd /d "%~dp0"

echo.
echo  ChurnShield - iniciando...
echo.

if not exist venv (
    echo  Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo  Erro: Python nao encontrado. Instale em https://python.org
        pause
        exit /b 1
    )
    call venv\Scripts\activate
    echo  Instalando dependencias...
    pip install -r requirements.txt -q
) else (
    call venv\Scripts\activate
)

if not exist .env (
    echo  Criando .env a partir do exemplo...
    copy .env.example .env >nul
)

echo  Abrindo http://localhost:8000
start http://localhost:8000

echo  Servidor rodando. Feche esta janela para parar.
echo.
venv\Scripts\python.exe -m uvicorn app.main:app --reload

pause
