@echo off
REM ============================================================================
REM INICIAR AUTONOMIA - Windows Batch Script
REM ============================================================================
REM
REM Este script inicia tanto el Backend (FastAPI) como el Frontend (React)
REM en ventanas separadas.
REM
REM Requisitos previos:
REM   - Python 3.8+ instalado
REM   - Node.js + npm instalado
REM   - Carpetas: backend_python/, autonomia-frontend/
REM
REM Uso:
REM   INICIAR.bat
REM
REM ============================================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Colores (para PowerShell sería más fácil, pero batch es limitado)
cls
echo.
echo ============================================================================
echo                    INICIANDO AUTONOMIA - Sistema Dual
echo ============================================================================
echo.
echo Backend:  FastAPI en puerto 8000 (http://localhost:8000)
echo Frontend: React+Vite en puerto 5173 (http://localhost:5173)
echo.
echo ============================================================================
echo.

REM Verificar que existen los directorios
if not exist "backend_python\" (
    echo [ERROR] Carpeta 'backend_python' no encontrada
    echo [INFO] Asegurate de estar en la raiz del proyecto
    pause
    exit /b 1
)

if not exist "autonomia-frontend\" (
    echo [ERROR] Carpeta 'autonomia-frontend' no encontrada
    echo [INFO] Asegurate de estar en la raiz del proyecto
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado en PATH
    echo [INFO] Instala Python desde https://www.python.org/
    pause
    exit /b 1
)

REM Verificar npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm no encontrado en PATH
    echo [INFO] Instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python y Node.js encontrados
echo.

REM ============================================================================
REM BACKEND
REM ============================================================================

echo [1/2] Iniciando Backend FastAPI...
echo.

start "Backend AutonomIA" cmd /k ^
    "cd backend_python && ^
    python -m venv venv 2>nul & ^
    call venv\Scripts\activate.bat && ^
    pip install -r requisitos.txt -q && ^
    echo. && ^
    echo ========================================== && ^
    echo Backend listo en http://localhost:8000 && ^
    echo Swagger en http://localhost:8000/docs && ^
    echo ========================================== && ^
    echo. && ^
    python -m uvicorn main:app --port 8000"

timeout /t 3 /nobreak

REM ============================================================================
REM FRONTEND
REM ============================================================================

echo [2/2] Iniciando Frontend React...
echo.

start "Frontend AutonomIA" cmd /k ^
    "cd autonomia-frontend && ^
    call npm install --silent --no-save 2>nul && ^
    echo. && ^
    echo ========================================== && ^
    echo Frontend listo en http://localhost:5173 && ^
    echo ========================================== && ^
    echo. && ^
    call npm run dev"

timeout /t 2 /nobreak

REM ============================================================================
REM INFO FINAL
REM ============================================================================

cls
echo.
echo ============================================================================
echo                    AUTONOMIA - Inicializado Exitosamente!
echo ============================================================================
echo.
echo BACKEND:   http://localhost:8000
echo FRONTEND:  http://localhost:5173
echo SWAGGER:   http://localhost:8000/docs
echo.
echo Para visualizar el dashboard, abre en navegador:
echo   http://localhost:5173
echo.
echo PROXIMOS PASOS:
echo   1. Espera 5-10 segundos mientras instala dependencias
echo   2. Abre http://localhost:5173 en navegador
echo   3. Verifica que los graficos carguen
echo   4. Para detener: cierra ambas ventanas (X en esquina)
echo.
echo NOTAS:
echo   - Se abrieron 2 ventanas nuevas (Backend + Frontend)
echo   - Mantenalas abiertas mientras uses la app
echo   - Los logs aparecen en consola
echo.
echo PROBLEMAS?
echo   - Ver: ACTIVAR-DESACTIVAR.md (seccion Problemas Comunes)
echo   - Backend logs: backend_python/logs/autonomia.log
echo   - Frontend logs: Ver consola (F12 en navegador)
echo.
echo ============================================================================
echo.

echo Presiona Enter para cerrar esta ventana...
pause

exit /b 0
