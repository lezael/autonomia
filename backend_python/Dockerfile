# Dockerfile para Backend AutonomIA
FROM python:3.11-slim

# Metadatos
LABEL maintainer="AutonomIA Team"
LABEL description="Analizador de Soberanía Tecnológica"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    AMBIENTE=produccion

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requisitos.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requisitos.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/salud || exit 1

# Ejecutar aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
