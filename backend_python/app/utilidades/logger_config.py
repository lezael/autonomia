"""
Configuración de logging para AutonomIA.
"""
import logging
import sys
from pathlib import Path
import os

# Crear directorio de logs si no existe
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configurar UTF-8 en Windows
if sys.platform == "win32":
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # Forzar UTF-8 en stdout
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Configurar logger
logger_app = logging.getLogger("autonomia")
logger_app.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Handler para archivo
file_handler = logging.FileHandler(LOG_DIR / "autonomia.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Formato de logs (sin emojis para evitar problemas de encoding en Windows)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger_app.addHandler(console_handler)
logger_app.addHandler(file_handler)
