#!/usr/bin/env python
"""Script de verificación rápida de medidas de seguridad."""
import os
import sys
from pathlib import Path


def check_file_exists(path: str, description: str) -> bool:
    """Verificar que un archivo existe."""
    exists = Path(path).exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists


def check_content_in_file(path: str, content: str, description: str) -> bool:
    """Verificar que un archivo contiene un contenido específico."""
    try:
        with open(path, 'r') as f:
            text = f.read()
            found = content.lower() in text.lower()
            status = "✅" if found else "❌"
            print(f"{status} {description}")
            return found
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False


def main():
    """Ejecutar verificación de seguridad."""
    print("=" * 70)
    print("🔒 VERIFICACIÓN DE SEGURIDAD - AutonomIA")
    print("=" * 70)
    print()
    
    results = []
    
    # 1. Archivos de configuración
    print("📦 ARCHIVOS DE CONFIGURACIÓN:")
    print("-" * 70)
    results.append(check_file_exists(
        "backend_python/.env.example",
        "Archivo .env.example (template de configuración)"
    ))
    results.append(check_file_exists(
        "backend_python/generar_configuracion.py",
        "Script generador de configuración segura"
    ))
    print()
    
    # 2. Documentación de seguridad
    print("📚 DOCUMENTACIÓN DE SEGURIDAD:")
    print("-" * 70)
    results.append(check_file_exists(
        "SEGURIDAD.md",
        "Documentación técnica SEGURIDAD.md"
    ))
    results.append(check_file_exists(
        "GUIA_SEGURIDAD.md",
        "Guía práctica GUIA_SEGURIDAD.md"
    ))
    results.append(check_file_exists(
        "CAMBIOS_SEGURIDAD.md",
        "Resumen de cambios CAMBIOS_SEGURIDAD.md"
    ))
    print()
    
    # 3. Validar main.py
    print("🔐 VALIDACIÓN DE main.py:")
    print("-" * 70)
    results.append(check_content_in_file(
        "backend_python/main.py",
        "from slowapi import Limiter",
        "Rate limiting import"
    ))
    results.append(check_content_in_file(
        "backend_python/main.py",
        "from dotenv import load_dotenv",
        "Environment variables import"
    ))
    results.append(check_content_in_file(
        "backend_python/main.py",
        "validar_url_segura",
        "SSRF protection validation"
    ))
    results.append(check_content_in_file(
        "backend_python/main.py",
        "@limiter.limit",
        "Rate limit decorator"
    ))
    results.append(check_content_in_file(
        "backend_python/main.py",
        "validar_api_key",
        "API Key authentication"
    ))
    print()
    
    # 4. Validar validadores.py
    print("✔️  VALIDACIÓN DE validadores.py:")
    print("-" * 70)
    results.append(check_content_in_file(
        "backend_python/app/utilidades/validadores.py",
        "validar_url_segura",
        "SSRF protection function"
    ))
    results.append(check_content_in_file(
        "backend_python/app/utilidades/validadores.py",
        "ipaddress",
        "IP address validation"
    ))
    results.append(check_content_in_file(
        "backend_python/app/utilidades/validadores.py",
        "192.168",
        "Private IP blocking"
    ))
    results.append(check_content_in_file(
        "backend_python/app/utilidades/validadores.py",
        "http",
        "Protocol restriction"
    ))
    print()
    
    # 5. Validar manejador_peticiones.py
    print("🌐 VALIDACIÓN DE manejador_peticiones.py:")
    print("-" * 70)
    results.append(check_content_in_file(
        "backend_python/app/extraccion/manejador_peticiones.py",
        "MAX_SIZE_BYTES",
        "Size limit constant"
    ))
    results.append(check_content_in_file(
        "backend_python/app/extraccion/manejador_peticiones.py",
        "text/html",
        "Content-Type validation"
    ))
    results.append(check_content_in_file(
        "backend_python/app/extraccion/manejador_peticiones.py",
        "stream=True",
        "Stream download method"
    ))
    results.append(check_content_in_file(
        "backend_python/app/extraccion/manejador_peticiones.py",
        "Content-Length",
        "Content-Length validation"
    ))
    print()
    
    # 6. Validar requisitos.txt
    print("📋 VALIDACIÓN DE requisitos.txt:")
    print("-" * 70)
    results.append(check_content_in_file(
        "backend_python/requisitos.txt",
        "slowapi",
        "slowapi dependency"
    ))
    results.append(check_content_in_file(
        "backend_python/requisitos.txt",
        "python-dotenv",
        "python-dotenv dependency"
    ))
    results.append(check_content_in_file(
        "backend_python/requisitos.txt",
        "ipaddress",
        "ipaddress dependency"
    ))
    print()
    
    # 7. Validar .gitignore
    print("🔒 VALIDACIÓN DE .gitignore:")
    print("-" * 70)
    results.append(check_content_in_file(
        ".gitignore",
        ".env",
        ".env protection"
    ))
    results.append(check_content_in_file(
        ".gitignore",
        "API_KEY",
        "API_KEY protection"
    ))
    results.append(check_content_in_file(
        ".gitignore",
        "secrets",
        "Secrets protection"
    ))
    print()
    
    # Resumen
    print("=" * 70)
    total = len(results)
    passed = sum(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"📊 RESUMEN: {passed}/{total} verificaciones pasadas ({percentage:.1f}%)")
    
    if percentage == 100:
        print("🎉 TODAS LAS MEDIDAS DE SEGURIDAD IMPLEMENTADAS CORRECTAMENTE")
        return 0
    elif percentage >= 80:
        print("✅ MAYORÍA DE MEDIDAS IMPLEMENTADAS - REVISAR FALTANTES")
        return 1
    else:
        print("❌ VERIFICAR IMPLEMENTACIÓN DE SEGURIDAD")
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(3)
