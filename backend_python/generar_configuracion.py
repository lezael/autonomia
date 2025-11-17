#!/usr/bin/env python
"""Script para generar configuración segura de AutonomIA."""
import secrets
import os
from pathlib import Path


def generar_api_key(longitud: int = 32) -> str:
    """Genera una API key segura aleatoria."""
    return secrets.token_urlsafe(longitud)


def crear_archivo_env(ruta_env: str = ".env", api_key: str = None):
    """
    Crea archivo .env con configuración segura.
    
    Args:
        ruta_env: Ruta donde guardar el archivo .env
        api_key: API key a usar (genera una si es None)
    """
    if api_key is None:
        api_key = generar_api_key()
    
    contenido_env = f"""# AutonomIA - Configuración de Seguridad
# Generado automáticamente - GUARDAR EN LUGAR SEGURO

# API Key para autenticación (cambiar periódicamente en producción)
API_KEY={api_key}

# Configuración del servidor
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autonomia.log
"""
    
    ruta_path = Path(ruta_env)
    
    # Verificar si ya existe
    if ruta_path.exists():
        print(f"⚠️  Archivo {ruta_env} ya existe. No se sobrescribe.")
        return False
    
    # Crear archivo con permisos restrictivos
    with open(ruta_env, 'w') as f:
        f.write(contenido_env)
    
    # Cambiar permisos a 600 (solo lectura/escritura para propietario)
    os.chmod(ruta_env, 0o600)
    
    print(f"✅ Archivo {ruta_env} creado exitosamente")
    print(f"📌 Permisos: 600 (solo propietario)")
    return True


def main():
    """Función principal."""
    import sys
    
    print("=" * 60)
    print("AutonomIA - Generador de Configuración de Seguridad")
    print("=" * 60)
    print()
    
    # Generar API key
    print("🔑 Generando API key segura...")
    api_key = generar_api_key(32)
    print(f"   API Key generada: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Preguntar dónde guardar
    ruta_env = input("Ruta para archivo .env [.env]: ").strip() or ".env"
    
    # Crear archivo
    if crear_archivo_env(ruta_env, api_key):
        print()
        print("✅ Configuración completada")
        print()
        print("📝 Próximos pasos:")
        print(f"   1. Guardar la API key en lugar seguro:")
        print(f"      {api_key}")
        print(f"   2. Verificar archivo: {ruta_env}")
        print(f"   3. Incluir en .gitignore (no commitar claves)")
        print(f"   4. Iniciar servidor:")
        print(f"      python -m uvicorn main:app --reload")
    else:
        print()
        print("❌ No se pudo crear configuración")
        sys.exit(1)


if __name__ == "__main__":
    main()
