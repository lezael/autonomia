"""
Punto de entrada principal - AutonomIA Backend
Infraestructura general lista para que tu colega integre análisis.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.endpoints import router as router_api
from app.utilidades.logger_config import logger_app


# ============================================================================
# CONFIGURACIÓN DE FASTAPI
# ============================================================================

def crear_app() -> FastAPI:
    """
    Factory function para crear la aplicación FastAPI.
    
    Returns:
        FastAPI: Aplicación configurada
    """
    
    app = FastAPI(
        title="AutonomIA API",
        description="Analizador de Soberanía Tecnológica - Backend",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # ========================================================================
    # CORS - Permitir frontend en desarrollo
    # ========================================================================
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",      # Vite dev server (frontend React)
            "http://localhost:5174",      # Vite puerto alternativo
            "http://localhost:3000",      # Alternativa
            "http://localhost:8000",      # Backend mismo
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],              # Permitir GET, POST, OPTIONS, etc
        allow_headers=["*"],              # Permitir cualquier header
    )
    
    logger_app.info("CORS habilitado para desarrollo (localhost:5173, 3000, 8000)")
    
    # ========================================================================
    # INCLUIR ROUTERS
    # ========================================================================
    
    app.include_router(router_api)
    logger_app.info("Routers incluidos en la aplicación")
    
    # ========================================================================
    # EVENTOS DE CICLO DE VIDA
    # ========================================================================
    
    @app.on_event("startup")
    async def startup_event():
        """Evento al iniciar el servidor"""
        logger_app.info("=" * 70)
        logger_app.info("[STARTUP] AutonomIA Backend iniciado")
        logger_app.info("=" * 70)
        logger_app.info("[INFO] API disponible en: http://localhost:8000")
        logger_app.info("[INFO] Documentacion en: http://localhost:8000/docs")
        logger_app.info("[INFO] Frontend React: http://localhost:5173")
        logger_app.info("=" * 70)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Evento al apagar el servidor"""
        logger_app.info("[SHUTDOWN] AutonomIA Backend detenido")
    
    return app


# ============================================================================
# CREAR INSTANCIA DE LA APP
# ============================================================================

app = crear_app()


# ============================================================================
# ENDPOINT ROOT (para verificar que el servidor responde)
# ============================================================================

@app.get("/", tags=["root"])
async def root():
    """
    Endpoint raíz para verificar que el servidor está corriendo.
    """
    return {
        "nombre": "AutonomIA Backend",
        "version": "1.0.0",
        "estado": "operacional",
        "documentacion": "/docs",
        "endpoints": {
            "salud": "/api/salud",
            "tecnologias": "/api/tecnologias",
            "analizar": "/api/analizar",
            "radar": "/api/radar-dependencia",
            "instituciones": "/api/instituciones",
            "matriz": "/api/matriz-dependencia",
        }
    }


# ============================================================================
# MAIN - Para ejecutar con: python main.py
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Configuración para desarrollo
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,              # Auto-reload en cambios
        log_level="info",
    )
