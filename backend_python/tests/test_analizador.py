"""
Tests para el analizador de soberanía tecnológica.
Verifica que todos los métodos matemáticos funcionen correctamente.
"""
import pytest
from app.analisis.analizador import analizador, TECNOLOGIAS_CONOCIDAS
from app.api.modelos import Tecnologia, TipoTecnologia


# ============================================================================
# FIXTURES (datos de prueba reutilizables)
# ============================================================================

@pytest.fixture
def html_con_google_analytics():
    """HTML que contiene Google Analytics"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://www.google-analytics.com/analytics.js"></script>
        <script async src="https://www.googletagmanager.com/gtag/js"></script>
    </head>
    <body>
        <h1>Test Page</h1>
    </body>
    </html>
    """


@pytest.fixture
def html_con_moodle():
    """HTML que contiene Moodle"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/theme/boost/style.css">
    </head>
    <body>
        <div class="moodle-container">
            <h1>Plataforma Educativa</h1>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def html_mixto():
    """HTML con tecnologías libres y privativas"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://google-analytics.com/analytics.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Roboto" rel="stylesheet">
        <script src="/wp-content/themes/theme.js"></script>
        <link rel="stylesheet" href="/theme/boost/style.css">
    </head>
    <body>
        <div class="moodle-container">
            <h1>Universidad</h1>
        </div>
    </body>
    </html>
    """


@pytest.fixture
def tecnologias_ejemplo():
    """Lista de tecnologías de ejemplo"""
    return [
        Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS"),
        Tecnologia(nombre="WordPress", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="CMS"),
        Tecnologia(nombre="Google Analytics", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="AWS CloudFront", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
    ]


# ============================================================================
# TEST 1: DETECTAR TECNOLOGÍAS
# ============================================================================

def test_detectar_tecnologias_google_analytics(html_con_google_analytics):
    """Debe detectar Google Analytics en el HTML"""
    tecnologias = analizador.detectar_tecnologias(html_con_google_analytics)
    
    nombres = [t.nombre for t in tecnologias]
    
    assert len(tecnologias) > 0, "Debería detectar al menos una tecnología"
    assert "Google Analytics" in nombres or "Google Tag Manager" in nombres, \
        "Debería detectar tecnologías de Google"
    
    # Verificar que son privativas
    for tech in tecnologias:
        assert tech.tipo == TipoTecnologia.PRIVATIVO, \
            f"{tech.nombre} debería ser PRIVATIVO"


def test_detectar_tecnologias_moodle(html_con_moodle):
    """Debe detectar Moodle en el HTML"""
    tecnologias = analizador.detectar_tecnologias(html_con_moodle)
    
    nombres = [t.nombre for t in tecnologias]
    
    assert "Moodle" in nombres, "Debería detectar Moodle"
    
    # Verificar que es libre
    moodle = next(t for t in tecnologias if t.nombre == "Moodle")
    assert moodle.tipo == TipoTecnologia.LIBRE, "Moodle debería ser LIBRE"


def test_detectar_tecnologias_mixtas(html_mixto):
    """Debe detectar tecnologías libres y privativas"""
    tecnologias = analizador.detectar_tecnologias(html_mixto)
    
    libres = [t for t in tecnologias if t.tipo == TipoTecnologia.LIBRE]
    privativas = [t for t in tecnologias if t.tipo == TipoTecnologia.PRIVATIVO]
    
    assert len(libres) > 0, "Debería detectar tecnologías libres"
    assert len(privativas) > 0, "Debería detectar tecnologías privativas"


def test_detectar_tecnologias_html_vacio():
    """HTML vacío no debería detectar tecnologías"""
    html_vacio = "<html><body></body></html>"
    tecnologias = analizador.detectar_tecnologias(html_vacio)
    
    assert len(tecnologias) == 0, "HTML vacío no debería detectar tecnologías"


# ============================================================================
# TEST 2: CALCULAR ÍNDICE DE SOBERANÍA
# ============================================================================

def test_calcular_indice_soberania_50_50():
    """50% libres, 50% privativas → S(i) = 0.5"""
    tecnologias = [
        Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS"),
        Tecnologia(nombre="WordPress", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="CMS"),
        Tecnologia(nombre="Google Analytics", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="AWS", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
    ]
    
    s_i = analizador.calcular_indice_soberania(tecnologias)
    
    assert s_i == 0.5, f"Debería ser 0.5, pero es {s_i}"


def test_calcular_indice_soberania_100_libres():
    """100% libres → S(i) = 1.0"""
    tecnologias = [
        Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS"),
        Tecnologia(nombre="WordPress", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="CMS"),
        Tecnologia(nombre="Apache", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="Servidor"),
    ]
    
    s_i = analizador.calcular_indice_soberania(tecnologias)
    
    assert s_i == 1.0, f"Debería ser 1.0, pero es {s_i}"


def test_calcular_indice_soberania_0_libres():
    """0% libres → S(i) = 0.0"""
    tecnologias = [
        Tecnologia(nombre="Google Analytics", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="AWS", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
    ]
    
    s_i = analizador.calcular_indice_soberania(tecnologias)
    
    assert s_i == 0.0, f"Debería ser 0.0, pero es {s_i}"


def test_calcular_indice_soberania_lista_vacia():
    """Lista vacía → S(i) = 0.0"""
    s_i = analizador.calcular_indice_soberania([])
    
    assert s_i == 0.0, "Lista vacía debería retornar 0.0"


# ============================================================================
# TEST 3: CALCULAR RANKING NORMALIZADO
# ============================================================================

def test_calcular_ranking_normalizado_0_5():
    """S(i) = 0.5 → R(i) = 0.5"""
    r_i = analizador.calcular_ranking_normalizado(0.5)
    
    assert r_i == 0.5, f"Debería ser 0.5, pero es {r_i}"


def test_calcular_ranking_normalizado_1_0():
    """S(i) = 1.0 → R(i) = 1.0"""
    r_i = analizador.calcular_ranking_normalizado(1.0)
    
    assert r_i == 1.0, f"Debería ser 1.0, pero es {r_i}"


def test_calcular_ranking_normalizado_0_0():
    """S(i) = 0.0 → R(i) = 0.0"""
    r_i = analizador.calcular_ranking_normalizado(0.0)
    
    assert r_i == 0.0, f"Debería ser 0.0, pero es {r_i}"


def test_calcular_ranking_normalizado_valor_invalido():
    """Valor fuera de rango [0, 1] debe lanzar ValueError"""
    with pytest.raises(ValueError):
        analizador.calcular_ranking_normalizado(1.5)
    
    with pytest.raises(ValueError):
        analizador.calcular_ranking_normalizado(-0.1)


# ============================================================================
# TEST 4: CONSTRUIR MATRIZ DE DEPENDENCIA
# ============================================================================

def test_construir_matriz_dependencia_4_tecnologias(tecnologias_ejemplo):
    """4 tecnologías → matriz [[1, 1, 1, 1]]"""
    matriz = analizador.construir_matriz_dependencia(tecnologias_ejemplo)
    
    assert len(matriz) == 1, "Debe tener 1 fila (esta institución)"
    assert len(matriz[0]) == 4, "Debe tener 4 columnas (4 tecnologías)"
    assert matriz[0] == [1, 1, 1, 1], "Todas las tecnologías detectadas deben tener valor 1"


def test_construir_matriz_dependencia_vacia():
    """Lista vacía → matriz [[]]"""
    matriz = analizador.construir_matriz_dependencia([])
    
    assert matriz == [[]], "Lista vacía debe retornar [[]]"


# ============================================================================
# TEST 5: GENERAR RECOMENDACIONES
# ============================================================================

def test_generar_recomendaciones_baja_soberania():
    """S(i) = 0.2 → Debe recomendar mejorar soberanía"""
    tecnologias = [
        Tecnologia(nombre="Google Analytics", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="AWS", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
        Tecnologia(nombre="Facebook", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Social"),
        Tecnologia(nombre="Microsoft", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Cloud"),
        Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS"),
    ]
    
    recomendaciones = analizador.generar_recomendaciones(tecnologias, 0.2)
    
    assert len(recomendaciones) > 0, "Debe generar recomendaciones"
    assert any("BAJA soberanía" in r for r in recomendaciones), \
        "Debe indicar que la soberanía es BAJA"


def test_generar_recomendaciones_alta_soberania():
    """S(i) = 0.9 → Debe felicitar"""
    tecnologias = [
        Tecnologia(nombre="Moodle", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="LMS"),
        Tecnologia(nombre="WordPress", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="CMS"),
        Tecnologia(nombre="Apache", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="Servidor"),
        Tecnologia(nombre="Nextcloud", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="Storage"),
        Tecnologia(nombre="Matomo", tipo=TipoTecnologia.LIBRE, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="Google Fonts", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
    ]
    
    recomendaciones = analizador.generar_recomendaciones(tecnologias, 0.83)
    
    assert any("Excelente" in r or "excelente" in r.lower() for r in recomendaciones), \
        "Debe felicitar por buena soberanía"


def test_generar_recomendaciones_sin_libres():
    """Sin tecnologías libres → Debe sugerir incorporarlas"""
    tecnologias = [
        Tecnologia(nombre="Google Analytics", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="Analítica"),
        Tecnologia(nombre="AWS", tipo=TipoTecnologia.PRIVATIVO, confianza=0.9, categoria="CDN"),
    ]
    
    recomendaciones = analizador.generar_recomendaciones(tecnologias, 0.0)
    
    assert any("libre" in r.lower() for r in recomendaciones), \
        "Debe sugerir incorporar tecnologías libres"


# ============================================================================
# TEST 6: VERIFICAR DICCIONARIO DE TECNOLOGÍAS
# ============================================================================

def test_tecnologias_conocidas_count():
    """Debe haber 20 tecnologías conocidas"""
    assert len(TECNOLOGIAS_CONOCIDAS) == 20, \
        f"Debe haber 20 tecnologías, hay {len(TECNOLOGIAS_CONOCIDAS)}"


def test_tecnologias_conocidas_balance():
    """Debe haber 10 libres y 10 privativas"""
    libres = sum(1 for t in TECNOLOGIAS_CONOCIDAS.values() 
                 if t['tipo'] == TipoTecnologia.LIBRE)
    privativas = sum(1 for t in TECNOLOGIAS_CONOCIDAS.values() 
                     if t['tipo'] == TipoTecnologia.PRIVATIVO)
    
    assert libres == 10, f"Debe haber 10 libres, hay {libres}"
    assert privativas == 10, f"Debe haber 10 privativas, hay {privativas}"


# ============================================================================
# TEST 7: INTEGRACIÓN COMPLETA
# ============================================================================

def test_flujo_completo_analisis(html_mixto):
    """Test de integración: flujo completo de análisis"""
    # 1. Detectar
    tecnologias = analizador.detectar_tecnologias(html_mixto)
    assert len(tecnologias) > 0, "Debe detectar tecnologías"
    
    # 2. Calcular S(i)
    indice = analizador.calcular_indice_soberania(tecnologias)
    assert 0.0 <= indice <= 1.0, "S(i) debe estar entre 0 y 1"
    
    # 3. Calcular R(i)
    ranking = analizador.calcular_ranking_normalizado(indice)
    assert 0.0 <= ranking <= 1.0, "R(i) debe estar entre 0 y 1"
    
    # 4. Construir matriz
    matriz = analizador.construir_matriz_dependencia(tecnologias)
    assert len(matriz) == 1, "Debe tener 1 fila"
    assert len(matriz[0]) == len(tecnologias), "Columnas = cantidad de tecnologías"
    
    # 5. Generar recomendaciones
    recomendaciones = analizador.generar_recomendaciones(tecnologias, indice)
    assert len(recomendaciones) > 0, "Debe generar recomendaciones"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])