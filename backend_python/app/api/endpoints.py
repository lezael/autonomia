"""
Endpoints de la API REST para AutonomIA.
Gestiona análisis de URLs y métricas de soberanía tecnológica.
"""
import time
from fastapi import APIRouter, HTTPException
from typing import List, Dict

from app.api.modelos import (
    SolicitudAnalisis,
    ResultadoAnalisis,
    RespuestaSalud,
    ListaTecnologias,
    TipoTecnologia
)
from app.extraccion.manejador_peticiones import obtener_contenido_url
from app.analisis.analizador import analizador
from app.utilidades.logger_config import logger_app


# ============================================================================
# ALMACENAMIENTO EN MEMORIA DE ANÁLISIS
# ============================================================================

# Almacenar los análisis realizados
analisis_realizados: List[Dict] = []


# ============================================================================
# ROUTER DE FASTAPI
# ============================================================================

router = APIRouter(
    prefix="/api",
    tags=["análisis"],
    responses={
        404: {"description": "No encontrado"},
        500: {"description": "Error interno del servidor"}
    }
)


# ============================================================================
# ENDPOINT: SALUD DEL SISTEMA
# ============================================================================

@router.get("/salud", response_model=RespuestaSalud)
async def verificar_salud():
    """
    Verifica que la API está funcionando correctamente.
    
    Returns:
        RespuestaSalud: Estado del sistema
        
    Example:
        GET /api/salud
        → {"estado": "ok", "mensaje": "Sistema operativo", "version": "1.0.0"}
    """
    return RespuestaSalud(
        estado="ok",
        mensaje="Sistema operativo - AutonomIA Backend",
        version="1.0.0"
    )


# ============================================================================
# ENDPOINT: ANÁLISIS DE URL
# ============================================================================

@router.post("/analizar", response_model=ResultadoAnalisis)
async def analizar_url(solicitud: SolicitudAnalisis):
    """
    Analiza dependencia tecnológica de una URL.
    
    FLUJO COMPLETO:
    1. ✅ Obtener contenido HTML
    2. ✅ Detectar tecnologías
    3. ✅ Calcular S(i) - Índice de Soberanía
    4. ✅ Calcular R(i) - Ranking Normalizado
    5. ✅ Construir matriz de dependencia
    6. ✅ Generar recomendaciones personalizadas
    
    Args:
        solicitud: SolicitudAnalisis con URL a analizar
        
    Returns:
        ResultadoAnalisis: Análisis completo con métricas
        
    Raises:
        HTTPException: 400 si URL no accesible, 500 si error interno
        
    Example:
        POST /api/analizar
        Body: {"url": "https://www.example.edu"}
        
        → {
            "url": "https://www.example.edu",
            "indice_soberania": 0.65,
            "ranking_normalizado": 0.65,
            "tecnologias_detectadas": [...],
            "tecnologias_libres_count": 13,
            "tecnologias_privativas_count": 7,
            "matriz_dependencia": [[1, 1, 0, ...]],
            "recomendaciones": ["...", "..."],
            "estado": "éxito",
            "mensaje": "Análisis completado: 20 tecnologías detectadas",
            "tiempo_procesamiento_ms": 1234
        }
    """
    inicio = time.time()
    url_str = str(solicitud.url)
    
    logger_app.info(f"📊 Iniciando análisis de URL: {url_str}")
    
    try:
        # ========================================
        # PASO 1: OBTENER CONTENIDO HTML
        # ========================================
        exito, contenido_html, error_msg = obtener_contenido_url(url_str)
        
        if not exito:
            logger_app.warning(f"❌ No se pudo acceder a {url_str}: {error_msg}")
            raise HTTPException(
                status_code=400,
                detail=f"No se pudo acceder a la URL: {error_msg}"
            )
        
        logger_app.info(f"✅ HTML descargado: {len(contenido_html)} caracteres")
        
        # ========================================
        # PASO 2: DETECTAR TECNOLOGÍAS
        # ========================================
        tecnologias = analizador.detectar_tecnologias(contenido_html)
        logger_app.info(f"🔍 Tecnologías detectadas: {len(tecnologias)}")
        
        # ========================================
        # PASO 3: CALCULAR ÍNDICE DE SOBERANÍA
        # ========================================
        indice_soberania = analizador.calcular_indice_soberania(tecnologias)
        logger_app.info(f"📈 S(i) = {indice_soberania:.4f}")
        
        # ========================================
        # PASO 4: CALCULAR RANKING NORMALIZADO
        # ========================================
        ranking_normalizado = analizador.calcular_ranking_normalizado(indice_soberania)
        logger_app.info(f"⭐ R(i) = {ranking_normalizado:.4f} (escala 0-1)")
        
        # ========================================
        # PASO 5: CONSTRUIR MATRIZ DE DEPENDENCIA
        # ========================================
        matriz_dependencia = analizador.construir_matriz_dependencia(tecnologias)
        logger_app.info(f"🔢 Matriz: {len(matriz_dependencia)}x{len(matriz_dependencia[0]) if matriz_dependencia else 0}")
        
        # ========================================
        # PASO 6: GENERAR RECOMENDACIONES
        # ========================================
        recomendaciones = analizador.generar_recomendaciones(tecnologias, indice_soberania)
        logger_app.info(f"💡 Recomendaciones generadas: {len(recomendaciones)}")
        
        # ========================================
        # PASO 7: CONTAR TECNOLOGÍAS POR TIPO
        # ========================================
        tecnologias_libres = sum(1 for t in tecnologias if t.tipo == TipoTecnologia.LIBRE)
        tecnologias_privativas = sum(1 for t in tecnologias if t.tipo == TipoTecnologia.PRIVATIVO)
        
        logger_app.info(f"📊 Libres: {tecnologias_libres} | Privativas: {tecnologias_privativas}")
        
        # ========================================
        # PASO 8: CREAR RESULTADO FINAL
        # ========================================
        tiempo_ms = int((time.time() - inicio) * 1000)
        
        resultado = ResultadoAnalisis(
            url=url_str,
            indice_soberania=indice_soberania,
            ranking_normalizado=ranking_normalizado,
            tecnologias_detectadas=tecnologias,
            tecnologias_libres_count=tecnologias_libres,
            tecnologias_privativas_count=tecnologias_privativas,
            matriz_dependencia=matriz_dependencia,
            recomendaciones=recomendaciones,
            estado="éxito",
            mensaje=f"Análisis completado: {len(tecnologias)} tecnologías detectadas",
            tiempo_procesamiento_ms=tiempo_ms
        )
        
        logger_app.info(f"✅ Análisis completado en {tiempo_ms}ms")
        
        # Guardar análisis en memoria
        analisis_realizados.append({
            "nombre": url_str.split('/')[2] if len(url_str.split('/')) > 2 else url_str,
            "url": url_str,
            "indice_soberania": indice_soberania,
            "ranking_normalizado": ranking_normalizado,
            "tecnologias": tecnologias,
            "tecnologias_libres_count": tecnologias_libres,
            "tecnologias_privativas_count": tecnologias_privativas,
            "matriz_dependencia": matriz_dependencia,
            "timestamp": time.time()
        })
        
        # Mantener solo los últimos 10 análisis
        if len(analisis_realizados) > 10:
            analisis_realizados.pop(0)
        
        return resultado
        
    except HTTPException:
        # Re-lanzar excepciones HTTP (400, 404, etc)
        raise
        
    except Exception as e:
        # Capturar errores inesperados
        tiempo_ms = int((time.time() - inicio) * 1000)
        logger_app.error(f"❌ Error inesperado: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


# ============================================================================
# ENDPOINT: LISTAR TECNOLOGÍAS CONOCIDAS
# ============================================================================

@router.get("/tecnologias", response_model=ListaTecnologias)
async def listar_tecnologias():
    """
    Lista todas las tecnologías que el sistema puede detectar.
    
    Returns:
        ListaTecnologias: Catálogo completo de tecnologías
        
    Example:
        GET /api/tecnologias
        
        → {
            "total": 20,
            "libres": 10,
            "privativas": 10,
            "tecnologias": [
                {"nombre": "Moodle", "tipo": "libre", "categoria": "LMS"},
                {"nombre": "Google Analytics", "tipo": "privativo", "categoria": "Analítica"},
                ...
            ]
        }
    """
    from app.analisis.analizador import TECNOLOGIAS_CONOCIDAS
    
    tecnologias = []
    
    for nombre, config in TECNOLOGIAS_CONOCIDAS.items():
        tecnologias.append({
            "nombre": nombre,
            "tipo": config['tipo'].value,  # Convertir Enum a string
            "categoria": config['categoria']
        })
    
    libres = sum(1 for t in tecnologias if t['tipo'] == 'libre')
    privativas = sum(1 for t in tecnologias if t['tipo'] == 'privativo')
    
    return ListaTecnologias(
        total=len(tecnologias),
        libres=libres,
        privativas=privativas,
        tecnologias=tecnologias
    )


# ============================================================================
# ENDPOINT: ESTADÍSTICAS DEL SISTEMA
# ============================================================================

@router.get("/estadisticas")
async def obtener_estadisticas():
    """
    Obtiene estadísticas generales del sistema.
    
    Returns:
        dict: Estadísticas del analizador
        
    Example:
        GET /api/estadisticas
        
        → {
            "tecnologias_conocidas": 20,
            "categorias": ["Analítica", "LMS", "CMS", "CDN", ...],
            "version_analizador": "1.0.0"
        }
    """
    from app.analisis.analizador import TECNOLOGIAS_CONOCIDAS
    
    categorias = set(config['categoria'] for config in TECNOLOGIAS_CONOCIDAS.values())
    
    return {
        "tecnologias_conocidas": len(TECNOLOGIAS_CONOCIDAS),
        "categorias": sorted(list(categorias)),
        "version_analizador": "1.0.0",
        "estado": "operativo"
    }


# ============================================================================
# ENDPOINTS ADICIONALES (para frontend)
# ============================================================================

# 1. /api/radar-dependencia
@router.get("/radar-dependencia")
async def obtener_radar_dependencia():
    """Retorna datos para el gráfico de radar basado en análisis reales"""
    if not analisis_realizados:
        # Datos de ejemplo si no hay análisis
        return {
            "categorias": ["Analítica", "CDN", "CMS", "LMS", "Hosting"],
            "series": [
                {
                    "nombre": "Sin análisis aún",
                    "data": [0, 0, 0, 0, 0]
                }
            ]
        }
    
    # Obtener categorías únicas de todas las tecnologías
    todas_categorias = set()
    for analisis in analisis_realizados:
        for tech in analisis['tecnologias']:
            todas_categorias.add(tech.categoria)
    
    categorias = sorted(list(todas_categorias))[:5]  # Máximo 5 categorías
    
    # Crear series con conteo de tecnologías privativas por categoría
    series = []
    for analisis in analisis_realizados[-3:]:  # Últimos 3 análisis
        data = []
        for cat in categorias:
            count = sum(1 for t in analisis['tecnologias'] 
                       if t.categoria == cat and t.tipo == TipoTecnologia.PRIVATIVO)
            data.append(count)
        
        series.append({
            "nombre": analisis['nombre'],
            "data": data
        })
    
    return {
        "categorias": categorias,
        "series": series
    }


# 2. /api/instituciones (ARRAY DIRECTO)
@router.get("/instituciones")
async def obtener_instituciones():
    """Retorna lista de instituciones analizadas"""
    if not analisis_realizados:
        # Datos de ejemplo si no hay análisis
        return [
            {
                "nombre": "Sin análisis aún",
                "url": "Analiza una URL primero",
                "indice_soberania": 0.0,
                "ranking_normalizado": 0.0
            }
        ]
    
    # Retornar análisis reales
    return [
        {
            "nombre": a['nombre'],
            "url": a['url'],
            "indice_soberania": a['indice_soberania'],
            "ranking_normalizado": a['ranking_normalizado']
        }
        for a in analisis_realizados
    ]


# 3. /api/matriz-dependencia
@router.get("/matriz-dependencia")
async def obtener_matriz_dependencia():
    """Retorna matriz de dependencia basada en análisis reales"""
    if not analisis_realizados:
        # Datos de ejemplo si no hay análisis
        return {
            "instituciones": ["Sin análisis"],
            "tecnologias": ["Analiza URLs primero"],
            "series": [
                {
                    "name": "Sin datos",
                    "data": [0]
                }
            ]
        }
    
    # Obtener todas las tecnologías únicas
    todas_tecnologias = set()
    for analisis in analisis_realizados:
        for tech in analisis['tecnologias']:
            todas_tecnologias.add(tech.nombre)
    
    tecnologias = sorted(list(todas_tecnologias))[:10]  # Máximo 10 tecnologías
    
    # Crear series con matriz de dependencia
    series = []
    for analisis in analisis_realizados:
        data = []
        for tech_nombre in tecnologias:
            # 1 si la institución usa la tecnología, 0 si no
            usa = 1 if any(t.nombre == tech_nombre for t in analisis['tecnologias']) else 0
            data.append(usa)
        
        series.append({
            "name": analisis['nombre'],
            "data": data
        })
    
    return {
        "instituciones": [a['nombre'] for a in analisis_realizados],
        "tecnologias": tecnologias,
        "series": series
    }
