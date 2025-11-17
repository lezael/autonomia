@echo off
REM Script de inicio para AutonomIA (Windows)
REM Este script configura e inicia el backend y frontend

echo.
echo ========================================
echo   AutonomIA - Analizador de Soberania
echo   Iniciador de Desarrollo (Windows)
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en PATH
    echo Descargalo desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar PHP
php --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] PHP no esta instalado o no esta en PATH
    echo El frontend no podra ejecutarse localmente
)

REM Navegar al backend
cd /d "%~dp0backend_python"

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [*] Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [*] Verificando dependencias...
pip install -q -r requisitos.txt

REM Iniciar backend
echo.
echo [✓] Iniciando backend FastAPI...
echo [*] Backend disponible en: http://localhost:8000
echo [*] Documentacion en: http://localhost:8000/docs
echo.
python main.py

pause
