#!/bin/bash
# Script de inicio para AutonomIA (Linux/Mac)
# Este script configura e inicia el backend

echo ""
echo "========================================"
echo "  AutonomIA - Analizador de Soberanía"
echo "  Iniciador de Desarrollo (Linux/Mac)"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 no está instalado"
    echo "Instálalo con: sudo apt-get install python3-pip (Debian/Ubuntu)"
    exit 1
fi

# Verificar PHP
if ! command -v php &> /dev/null; then
    echo "[ADVERTENCIA] PHP no está instalado"
    echo "El frontend no podrá ejecutarse localmente"
fi

# Navegar al backend
cd "$(dirname "$0")/backend_python"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "[*] Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "[*] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[*] Verificando dependencias..."
pip install -q -r requisitos.txt

# Iniciar backend
echo ""
echo "[✓] Iniciando backend FastAPI..."
echo "[*] Backend disponible en: http://localhost:8000"
echo "[*] Documentación en: http://localhost:8000/docs"
echo ""
python main.py
