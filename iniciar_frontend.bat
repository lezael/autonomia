@echo off
REM Script de inicio para Frontend PHP (Windows)

echo.
echo ========================================
echo   AutonomIA - Frontend PHP
echo   Servidor de Desarrollo (Windows)
echo ========================================
echo.

REM Verificar PHP
php --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PHP no esta instalado o no esta en PATH
    echo Descargalo desde: https://www.php.net/downloads
    pause
    exit /b 1
)

REM Navegar al frontend
cd /d "%~dp0frontend_php"

echo [*] Iniciando servidor PHP built-in...
echo.
echo [✓] Frontend disponible en: http://localhost:8080
echo [*] Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar servidor PHP
php -S localhost:8080

pause
