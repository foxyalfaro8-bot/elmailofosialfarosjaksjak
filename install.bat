@echo off
setlocal enabledelayedexpansion

echo [CHECK] Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no instalado
    echo Descarga: https://www.python.org/downloads/
    echo Marca Add Python to PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo [OK] Python %%i

echo [CHECK] pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no encontrado
    python -m ensurepip --upgrade
)
echo [OK] pip listo

echo.
echo [SETUP] venv...
if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: fallo venv
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: fallo activar venv
    pause
    exit /b 1
)

echo [INSTALL] dependencias...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: fallo instalar
    pause
    exit /b 1
)

echo [CHECK] sqlite...
if not exist data\ mkdir data

echo [DONE]
echo.
echo Para correr:
echo   venv\Scripts\activate.bat
echo   python main.py
echo.
pause
