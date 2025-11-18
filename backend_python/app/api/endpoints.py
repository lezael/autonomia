"""
Endpoints REST de la API AutonomIA.
Infraestructura general - Tu colega implementará la lógica de análisis específica.
"""
from fastapi import APIRouter, HTTPException, Query
import time
from typing import List

from app.api.modelos import (
    SolicitudAnalisis,
    ResultadoAnalisis,
    RespuestaSalud,
    ListaTecnologias,
    DatosRadar,
    DatosTablaInstituciones,
    DatosMatrizDependencia,
    SerieHeatmap,
    Tecnologia,
    TipoTecnologia
)
from app.extraccion.manejador_peticiones import obtener_contenido_url

# Router para endpoints de la API
router = APIRouter(prefix="/api", tags=["api"])


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/salud", response_model=RespuestaSalud)
async def health_check():
    """
    Verifica el estado del servidor.
    
    Returns:
        RespuestaSalud: Estado operacional de la API
    """
    return RespuestaSalud(
        status="operacional",
        version="1.0.0",
        mensaje="API AutonomIA operacional"
    )


# ============================================================================
# LISTAR TECNOLOGÍAS
# ============================================================================

@router.get("/tecnologias", response_model=ListaTecnologias)
async def listar_tecnologias():
    """
    Lista todas las tecnologías detectables.
    
    Tu colega: Actualizar esta lista según detector_tecnologias.py
    
    Returns:
        ListaTecnologias: Tecnologías libres y privativas
    """
    libres = [
        "Moodle",
        "Nextcloud",
        "WordPress",
        "Jitsi Meet",
        "BigBlueButton",
        "LibreOffice Online",
        "Mattermost",
        "Rocket.Chat",
    ]
    
    privativas = [
        "Google Analytics",
        "Google Tag Manager",
        "Microsoft Azure",
        "AWS CloudFront",
        "Facebook Pixel",
        "LinkedIn Insight",
        "Google Fonts",
        "Salesforce",
        "Intercom",
        "Slack",
    ]
    
    return ListaTecnologias(
        libres=libres,
        privativas=privativas,
        total=len(libres) + len(privativas)
    )


# ============================================================================
# DATOS PARA GRÁFICOS (Ejemplo - tu colega los completará)
# ============================================================================

@router.get("/radar-dependencia", response_model=DatosRadar)
async def get_radar_dependencia():
    """
    Obtiene datos para gráfico de radar de dependencia.
    
    DATO DE EJEMPLO: Tu colega reemplazará con datos reales de BD/análisis
    
    Returns:
        DatosRadar: Etiquetas y valores de dependencia
    """
    return DatosRadar(
        labels=["Google", "AWS", "Microsoft", "Meta"],
        valoresDeDependencia=[2, 1, 2, 1]
    )


@router.get("/instituciones", response_model=List[DatosTablaInstituciones])
async def get_instituciones():
    """
    Obtiene ranking de instituciones (tabla de soberanía).
    
    DATO DE EJEMPLO: Tu colega reemplazará con datos reales
    
    Returns:
        List[DatosTablaInstituciones]: Instituciones con sus métricas
    """
    return [
        DatosTablaInstituciones(institucion="Univ_A", s=-25, r=3.5),
        DatosTablaInstituciones(institucion="Univ_B", s=67, r=8.2),
        DatosTablaInstituciones(institucion="Univ_C", s=-100, r=0.0),
    ]


@router.get("/matriz-dependencia", response_model=DatosMatrizDependencia)
async def get_matriz_dependencia():
    """
    Obtiene datos para heatmap de matriz de dependencia.
    
    DATO DE EJEMPLO: Tu colega reemplazará con matriz real calculada
    
    Returns:
        DatosMatrizDependencia: Series e instituciones
    """
    return DatosMatrizDependencia(
        series=[
            SerieHeatmap(name="Univ_A", data=[1, 0, 1, 0]),
            SerieHeatmap(name="Univ_B", data=[1, 1, 0, 0]),
            SerieHeatmap(name="Univ_C", data=[0, 0, 1, 1]),
        ],
        categorias=["Google", "AWS", "Microsoft", "Meta"]
    )


# ============================================================================
# ENDPOINT PRINCIPAL: ANALIZAR URL
# ============================================================================

@router.post("/analizar", response_model=ResultadoAnalisis)
async def analizar_url(solicitud: SolicitudAnalisis):
    """
    Analiza dependencia tecnológica de una URL.
    
    FLUJO:
    1. ✅ Obtener contenido HTML (implementado)
    2. ❌ Detectar tecnologías (TU COLEGA)
    3. ❌ Calcular índices (TU COLEGA)
    4. ❌ Construir matriz (TU COLEGA)
    5. ❌ Generar recomendaciones (TU COLEGA)
    
    Args:
        solicitud: URL a analizar
        
    Returns:
        ResultadoAnalisis: Análisis completo con métricas
        
    Raises:
        HTTPException: Si la URL no es accesible o hay error
    """
    inicio = time.time()
    url_str = str(solicitud.url)
    
    try:
        # PASO 1: Obtener contenido HTML
        exito, contenido_html, error_msg = obtener_contenido_url(url_str)
        
        if not exito:
            raise HTTPException(
                status_code=400,
                detail=f"No se pudo acceder a la URL: {error_msg}"
            )
        
        # PASO 2-5: TU COLEGA IMPLEMENTARÁ AQUÍ
        # Crear instancia de ResultadoAnalisis con los datos que tu colega calcule
        
        resultado = ResultadoAnalisis(
            url=url_str,
            indice_soberania=None,  # Tu colega: calcular
            ranking_normalizado=None,  # Tu colega: calcular
            tecnologias_detectadas=[],  # Tu colega: obtener de detector
            tecnologias_libres_count=0,  # Tu colega: contar
            tecnologias_privativas_count=0,  # Tu colega: contar
            matriz_dependencia=None,  # Tu colega: construir con NumPy
            recomendaciones=[],  # Tu colega: generar
            estado="éxito",
            mensaje="Análisis en desarrollo - estructura lista para tu colega",
            tiempo_procesamiento_ms=int((time.time() - inicio) * 1000)
        )
        
        return resultado
        
    except HTTPException:
        raise
    except Exception as e:
        tiempo_ms = int((time.time() - inicio) * 1000)
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


# ============================================================================
# ENDPOINT PARA DEBUG (opcional)
# ============================================================================

@router.post("/debug/analizar-html")
async def debug_analizar_html(solicitud: SolicitudAnalisis):
    """
    SOLO PARA DESARROLLO: Retorna HTML bruto de la URL.
    Tu colega puede usar esto para debuggear patrones de detección.
    
    Args:
        solicitud: URL a analizar
        
    Returns:
        dict: Con HTML bruto (limitado a 10KB para debug)
    """
    url_str = str(solicitud.url)
    exito, contenido_html, error_msg = obtener_contenido_url(url_str)
    
    if not exito:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Limitar a 10KB para respuesta JSON
    html_truncado = contenido_html[:10000]
    
    return {
        "url": url_str,
        "tamaño_bytes": len(contenido_html),
        "html_primeros_10kb": html_truncado,
        "completo": len(contenido_html) <= 10000
    }
