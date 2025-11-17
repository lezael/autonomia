#!/bin/bash
# Script de inicio para Frontend PHP (Linux/Mac)

echo ""
echo "========================================"
echo "  AutonomIA - Frontend PHP"
echo "  Servidor de Desarrollo (Linux/Mac)"
echo "========================================"
echo ""

# Verificar PHP
if ! command -v php &> /dev/null; then
    echo "[ERROR] PHP no está instalado"
    echo "Instálalo con: sudo apt-get install php-cli (Debian/Ubuntu)"
    echo "O desde: https://www.php.net/downloads"
    exit 1
fi

# Navegar al frontend
cd "$(dirname "$0")/frontend_php"

echo "[*] Iniciando servidor PHP built-in..."
echo ""
echo "[✓] Frontend disponible en: http://localhost:8080"
echo "[*] Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar servidor PHP
php -S localhost:8080
