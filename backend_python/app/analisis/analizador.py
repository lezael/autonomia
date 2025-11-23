"""
Módulo de análisis de soberanía tecnológica.
Implementa detección de tecnologías y cálculo de métricas.
"""
import time
import re
from typing import List, Dict
from app.api.modelos import Tecnologia, TipoTecnologia


# ============================================================================
# DICCIONARIO DE TECNOLOGÍAS CONOCIDAS
# ============================================================================

TECNOLOGIAS_CONOCIDAS = {
    # === TECNOLOGÍAS PRIVATIVAS ===
    "Google Analytics": {
        "patterns": [
            r"google-analytics\.com",
            r"analytics\.js",
            r"ga\.js",
            r"gtag",
        ],
        "categoria": "Analítica",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Google Tag Manager": {
        "patterns": [
            r"googletagmanager\.com",
            r"gtm\.js",
        ],
        "categoria": "Analítica",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Google Fonts": {
        "patterns": [
            r"fonts\.googleapis\.com",
            r"fonts\.gstatic\.com",
        ],
        "categoria": "CDN",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "AWS CloudFront": {
        "patterns": [
            r"cloudfront\.net",
            r"amazonaws\.com",
        ],
        "categoria": "CDN",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Microsoft Azure": {
        "patterns": [
            r"azure\.com",
            r"azureedge\.net",
        ],
        "categoria": "Hosting",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Facebook Pixel": {
        "patterns": [
            r"facebook\.com/tr",
            r"fbevents\.js",
            r"connect\.facebook\.net",
        ],
        "categoria": "Analítica",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "LinkedIn Insight": {
        "patterns": [
            r"linkedin\.com/px",
            r"snap\.licdn\.com",
        ],
        "categoria": "Analítica",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Salesforce": {
        "patterns": [
            r"salesforce\.com",
            r"force\.com",
        ],
        "categoria": "CRM",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Intercom": {
        "patterns": [
            r"intercom\.io",
            r"widget\.intercom\.io",
        ],
        "categoria": "Chat",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    "Slack": {
        "patterns": [
            r"slack\.com",
            r"slack-edge\.com",
        ],
        "categoria": "Chat",
        "tipo": TipoTecnologia.PRIVATIVO
    },
    
    # === TECNOLOGÍAS LIBRES ===
    "Moodle": {
        "patterns": [
            r"moodle",
            r"/theme/boost",
            r"/pluginfile\.php",
        ],
        "categoria": "LMS",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Nextcloud": {
        "patterns": [
            r"nextcloud",
            r"/apps/files",
        ],
        "categoria": "Almacenamiento",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "WordPress": {
        "patterns": [
            r"wp-content",
            r"wp-includes",
            r"wordpress",
        ],
        "categoria": "CMS",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Jitsi Meet": {
        "patterns": [
            r"jitsi",
            r"meet\.jit\.si",
        ],
        "categoria": "Videoconferencia",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "BigBlueButton": {
        "patterns": [
            r"bigbluebutton",
            r"bbb-",
        ],
        "categoria": "Videoconferencia",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "LibreOffice Online": {
        "patterns": [
            r"libreoffice",
            r"collabora",
        ],
        "categoria": "Ofimática",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Mattermost": {
        "patterns": [
            r"mattermost",
        ],
        "categoria": "Chat",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Rocket.Chat": {
        "patterns": [
            r"rocket\.chat",
            r"rocketchat",
        ],
        "categoria": "Chat",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Matomo": {
        "patterns": [
            r"matomo",
            r"piwik",
        ],
        "categoria": "Analítica",
        "tipo": TipoTecnologia.LIBRE
    },
    
    "Apache": {
        "patterns": [
            r"apache",
        ],
        "categoria": "Servidor",
        "tipo": TipoTecnologia.LIBRE
    },
}


# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class AnalizadorSoberania:
    """
    Clase principal para análisis de soberanía tecnológica.
    
    Implementa:
    - Detección de tecnologías (20 tecnologías)
    - Cálculo de S(i) - Índice de Soberanía
    - Cálculo de R(i) - Ranking Normalizado
    - Construcción de matriz D de dependencia
    - Generación de recomendaciones
    """
    
    def __init__(self):
        """Inicializa el analizador"""
        self.inicio_procesamiento = time.time()
    
    def detectar_tecnologias(self, contenido_html: str) -> List[Tecnologia]:
        """
        Detecta tecnologías en el HTML usando patrones regex.
        
        Args:
            contenido_html: HTML de la página a analizar
            
        Returns:
            List[Tecnologia]: Lista de tecnologías detectadas
            
        Example:
            >>> analizador = AnalizadorSoberania()
            >>> html = "<script src='https://google-analytics.com/analytics.js'></script>"
            >>> techs = analizador.detectar_tecnologias(html)
            >>> len(techs) > 0
            True
        """
        tecnologias_encontradas = []
        tecnologias_detectadas_nombres = set()  # Para evitar duplicados
        
        for nombre_tech, config in TECNOLOGIAS_CONOCIDAS.items():
            # Si ya detectamos esta tecnología, saltar
            if nombre_tech in tecnologias_detectadas_nombres:
                continue
            
            # Buscar cada patrón
            for pattern in config['patterns']:
                if re.search(pattern, contenido_html, re.IGNORECASE):
                    # ¡Encontrada!
                    tech = Tecnologia(
                        nombre=nombre_tech,  # ← Corregido de "name" a "nombre"
                        tipo=config['tipo'],  # ← Ahora es TipoTecnologia (Enum)
                        confianza=0.90,  # ← Corregido de "confidence" a "confianza"
                        categoria=config['categoria']
                    )
                    
                    tecnologias_encontradas.append(tech)
                    tecnologias_detectadas_nombres.add(nombre_tech)
                    break  # Ya encontramos esta tech, pasar a la siguiente
        
        return tecnologias_encontradas
    
    def calcular_indice_soberania(self, tecnologias: List[Tecnologia]) -> float:
        """
        Calcula índice de soberanía S(i).
        
        Fórmula:
        S(i) = Tecnologías Libres / Total Tecnologías
        
        Rango: 0.0 (100% dependiente) a 1.0 (100% soberano)
        
        Args:
            tecnologias: Lista de tecnologías detectadas
            
        Returns:
            float: Índice entre 0.0 y 1.0
            
        Example:
            >>> tech1 = Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS")
            >>> tech2 = Tecnologia(nombre="Google", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica")
            >>> s = analizador.calcular_indice_soberania([tech1, tech2])
            >>> round(s, 2)
            0.5
        """
        if not tecnologias:
            return 0.0  # Sin tecnologías = sin soberanía
        
        libres = sum(1 for t in tecnologias if t.tipo == TipoTecnologia.LIBRE)
        total = len(tecnologias)
        
        s_i = libres / total
        
        return round(s_i, 4)  # 4 decimales
    
    def calcular_ranking_normalizado(self, indice_soberania: float) -> float:
        """
        Calcula ranking normalizado R(i) en escala 0-1 (frontend lo multiplica por 10).
        
        Fórmula:
        R(i) = S(i)  (ya está en escala 0-1)
        
        Args:
            indice_soberania: Índice S(i) entre 0.0 y 1.0
            
        Returns:
            float: Ranking entre 0.0 y 1.0
            
        Example:
            >>> r = analizador.calcular_ranking_normalizado(0.65)
            >>> r
            0.65
        """
        # Validar rango
        if not (0.0 <= indice_soberania <= 1.0):
            raise ValueError(
                f"S(i) debe estar entre 0.0 y 1.0, recibido: {indice_soberania}"
            )
        
        # El modelo espera 0-1, no 0-10
        # Frontend lo convierte a escala 0-10 para visualización
        return round(indice_soberania, 4)
    
    def construir_matriz_dependencia(self, tecnologias: List[Tecnologia]) -> List[List[int]]:
        """
        Construye matriz de dependencia D[1 x n_tecnologias].
        
        Para una sola institución (esta URL analizada):
        - Filas: 1 (esta institución)
        - Columnas: n tecnologías detectadas
        - Valores: 1 (usa esta tecnología)
        
        Args:
            tecnologias: Tecnologías detectadas
            
        Returns:
            List[List[int]]: Matriz 1xN donde N = len(tecnologias)
            
        Example:
            >>> techs = [tech1, tech2, tech3]
            >>> matriz = analizador.construir_matriz_dependencia(techs)
            >>> matriz
            [[1, 1, 1]]
        """
        if not tecnologias:
            return [[]]
        
        # Matriz de 1 fila (esta institución) x N columnas (tecnologías detectadas)
        # Todas las tecnologías detectadas tienen valor 1 (las usa)
        fila = [1 for _ in tecnologias]
        
        return [fila]  # Lista de listas (matriz 1xN)
    
    def generar_recomendaciones(self, 
                               tecnologias: List[Tecnologia],
                               indice_soberania: float) -> List[str]:
        """
        Genera recomendaciones personalizadas basadas en análisis.
        
        Args:
            tecnologias: Tecnologías detectadas
            indice_soberania: Índice S(i)
            
        Returns:
            list[str]: Lista de recomendaciones en lenguaje natural
            
        Example:
            >>> recos = analizador.generar_recomendaciones(techs, 0.3)
            >>> len(recos) > 0
            True
        """
        recomendaciones = []
        r_i_display = indice_soberania * 10  # Convertir a escala 0-10 para mensaje
        
        # 1. Recomendación general basada en S(i)
        if r_i_display < 3:
            recomendaciones.append(
                f"⚠️ Tu institución tiene BAJA soberanía ({r_i_display:.1f}/10). "
                "Considera desarrollar una estrategia de migración a alternativas libres."
            )
        elif r_i_display < 6:
            recomendaciones.append(
                f"📊 Soberanía MEDIA ({r_i_display:.1f}/10). Identifica dependencias críticas "
                "y crea un plan de migración gradual hacia software libre."
            )
        else:
            recomendaciones.append(
                f"✅ ¡Excelente soberanía tecnológica ({r_i_display:.1f}/10)! "
                "Mantén esta estrategia de uso de tecnologías libres."
            )
        
        # 2. Recomendaciones específicas por tecnologías privativas
        propietarias = [t for t in tecnologias if t.tipo == TipoTecnologia.PRIVATIVO]
        
        for tech in propietarias[:3]:  # Top 3 privativas detectadas
            recomendaciones.append(
                f"⚠️ Dependencia detectada: {tech.nombre} ({tech.categoria}). "
                f"Evalúa alternativas libres (confianza: {tech.confianza:.0%})"
            )
        
        # 3. Mensaje positivo sobre tecnologías libres
        libres = [t for t in tecnologias if t.tipo == TipoTecnologia.LIBRE]
        
        if libres:
            nombres_libres = ", ".join([t.nombre for t in libres[:5]])  # Máximo 5
            recomendaciones.append(
                f"✅ Positivo: ya usas {len(libres)} tecnologías libres ({nombres_libres})"
            )
        else:
            recomendaciones.append(
                "💡 Sugerencia: No se detectaron tecnologías libres. "
                "Considera incorporar herramientas de código abierto como Moodle, Nextcloud, o Matomo."
            )
        
        return recomendaciones


# ============================================================================
# INSTANCIA GLOBAL (para importar desde endpoints.py)
# ============================================================================

analizador = AnalizadorSoberania()
