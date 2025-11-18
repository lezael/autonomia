# 🧮 GUÍA PARA COLEGA MATEMÁTICO - AutonomIA

**De**: Tu colega de backend (yo) | **Para**: Colega responsable de análisis matemático

**Fecha**: Noviembre 2025 | **Urgencia**: Media | **Complejidad**: Media-Alta

---

## 👋 Bienvenida

Te has sumado al equipo cuando la **infraestructura está al 100%**. Tu trabajo es el **corazón matemático** del sistema. Esto es una guía paso a paso.

### El Equipo

| Rol | Persona |
|-----|---------|
| Backend Infraestructura | Yo (TU COLEGA) |
| Frontend Diseño UI/UX | Colega 3 |
| Backend Matemática | **TÚ** |

### Tu Responsabilidad

Implementar **5 métodos matemáticos** que analizan URLs y retornan métricas de soberanía tecnológica.

---

## 🎯 Tu Misión

### En una frase
**Detectar tecnologías en un HTML, calcular grados de dependencia, y generar métricas de soberanía.**

### Desglosado

```
Input: URL (ej: http://www.uni.edu.ar)
         ↓
Paso 1: ✅ Descargar HTML [YA HECHO por mí]
         ↓
Paso 2: ⏳ Detectar tecnologías [TÚ]
         ↓
Paso 3: ⏳ Calcular S(i) [TÚ]
         ↓
Paso 4: ⏳ Calcular R(i) [TÚ]
         ↓
Paso 5: ⏳ Construir matriz D [TÚ]
         ↓
Paso 6: ⏳ Generar recomendaciones [TÚ]
         ↓
Output: Métricas (JSON)
```

---

## 📍 Dónde Trabajar

### El Archivo Principal

```
backend_python/app/analisis/analizador.py
```

### Estructura Actual

```python
class AnalizadorSoberania:
    """
    Clase que orquesta todo el análisis de soberanía.
    
    Métodos que ya existen (NO TOQUES):
        - __init__()
        - analizar_url()        # Orquestador principal
    
    Métodos que TÚ IMPLEMENTAS:
        - detectar_tecnologias()            # 🔴 TODO
        - calcular_indice_soberania()       # 🔴 TODO
        - calcular_ranking_normalizado()    # 🔴 TODO
        - construir_matriz_dependencia()    # 🔴 TODO
        - generar_recomendaciones()         # 🔴 TODO
    
    Métodos helper:
        - _extraer_patrones()               # Para detectar_tecnologias
        - _normalizar_score()               # Helpers si necesitas
    """
    
    async def analizar_url(self, url: str) -> dict:
        """
        ORQUESTADOR PRINCIPAL - YA IMPLEMENTADO
        
        Qué hace:
        1. Obtiene HTML (YA HECHO)
        2. Llama detectar_tecnologias() → TÚ IMPLEMENTAS
        3. Llama calcular_indice_soberania() → TÚ IMPLEMENTAS
        4. Llama calcular_ranking_normalizado() → TÚ IMPLEMENTAS
        5. Llama construir_matriz_dependencia() → TÚ IMPLEMENTAS
        6. Llama generar_recomendaciones() → TÚ IMPLEMENTAS
        7. Retorna diccionario con TODOS los resultados
        
        Tú NO necesitas tocar esto (ya está integrado)
        """
        pass
```

---

## 🔴 MÉTODO 1: detectar_tecnologias()

### Qué Hace

Busca en el HTML patrones de tecnologías (Google, AWS, Microsoft, Meta, etc).

### Signature

```python
def detectar_tecnologias(self, html: str) -> list[Tecnologia]:
    """
    Detecta qué tecnologías usa la institución en su HTML.
    
    Args:
        html (str): Contenido HTML de la página
    
    Returns:
        list[Tecnologia]: Lista de objetos Tecnologia encontrados
        
    Ejemplo:
        >>> analizador.detectar_tecnologias("<script src='...googleapis.com...'></script>")
        [Tecnologia(name="Google", tipo="privativo", confidence=0.95, categoria="analytics")]
    """
```

### Modelo Esperado

```python
# De: backend_python/app/api/modelos.py
class Tecnologia(BaseModel):
    name: str                    # "Google", "AWS", "Microsoft", etc
    tipo: str                    # "privativo" o "libre"
    confidence: float            # 0.0 a 1.0 (certeza de detección)
    categoria: str               # "analytics", "hosting", "cdn", etc
```

### Tecnologías a Detectar (Mínimo 18)

```python
TECNOLOGIAS_CONOCIDAS = {
    # Propietarias (tipo="privativo")
    "Google": {
        "patterns": [
            r"googleapis\.com",
            r"google-analytics",
            r"googlesyndication",
            r"gstatic\.com",
            r"google\.com/intl",
        ],
        "categoria": "analytics",
        "tipo": "privativo"
    },
    
    "AWS": {
        "patterns": [
            r"amazonaws\.com",
            r"s3\.amazonaws",
            r"cloudfront\.amazonaws",
        ],
        "categoria": "hosting",
        "tipo": "privativo"
    },
    
    "Microsoft": {
        "patterns": [
            r"microsoft\.com",
            r"msftconnecttest\.com",
            r"office365\.com",
            r"sharepoint\.com",
        ],
        "categoria": "productivity",
        "tipo": "privativo"
    },
    
    "Meta": {
        "patterns": [
            r"facebook\.com",
            r"instagram\.com",
            r"fbcdn\.net",
        ],
        "categoria": "social",
        "tipo": "privativo"
    },
    
    # Libres (tipo="libre")
    "Linux": {
        "patterns": [r"linux"],
        "categoria": "os",
        "tipo": "libre"
    },
    
    "Apache": {
        "patterns": [r"apache"],
        "categoria": "server",
        "tipo": "libre"
    },
    
    # ... 12+ tecnologías más
}
```

### Algoritmo

```python
def detectar_tecnologias(self, html: str) -> list[Tecnologia]:
    tecnologias_encontradas = []
    
    for nombre_tech, config in TECNOLOGIAS_CONOCIDAS.items():
        for pattern in config['patterns']:
            if re.search(pattern, html, re.IGNORECASE):
                # Encontré esta tecnología
                tech = Tecnologia(
                    name=nombre_tech,
                    tipo=config['tipo'],
                    confidence=0.85,  # Ajusta según seguridad del patrón
                    categoria=config['categoria']
                )
                
                # Evitar duplicados
                if tech not in tecnologias_encontradas:
                    tecnologias_encontradas.append(tech)
                
                break  # Encontrado este, siguiente tech
    
    return tecnologias_encontradas
```

### Pseudocódigo

```
1. Definir diccionario de patrones regex para 18+ tecnologías
2. Para cada tecnología:
   a. Para cada patrón:
      - Buscar patrón en HTML (case-insensitive)
      - Si encontrado:
        * Crear objeto Tecnologia
        * Agregar a lista (evitar duplicados)
        * Pasar a siguiente tech
3. Retornar lista de Tecnologia
```

### Output Esperado

```python
[
    Tecnologia(name="Google", tipo="privativo", confidence=0.95, categoria="analytics"),
    Tecnologia(name="AWS", tipo="privativo", confidence=0.90, categoria="hosting"),
    Tecnologia(name="Apache", tipo="libre", confidence=0.88, categoria="server"),
    ...  # Total: 5-15 tecnologías detectadas
]
```

---

## 🔴 MÉTODO 2: calcular_indice_soberania()

### Qué Hace

Calcula S(i) = grado de soberanía (0 a 1).

### Fórmula

```
S(i) = Número de tecnologías LIBRES
       ───────────────────────────────
       Total de tecnologías detectadas

Rango: 0.0 (sin soberanía) a 1.0 (máxima soberanía)

Ejemplos:
- 5 libres, 0 propietarias → S(i) = 5/5 = 1.0 (100%)
- 0 libres, 5 propietarias → S(i) = 0/5 = 0.0 (0%)
- 3 libres, 2 propietarias → S(i) = 3/5 = 0.6 (60%)
```

### Signature

```python
def calcular_indice_soberania(self, tecnologias: list[Tecnologia]) -> float:
    """
    Calcula el índice de soberanía S(i).
    
    Args:
        tecnologias (list[Tecnologia]): Tecnologías detectadas
    
    Returns:
        float: Valor entre 0.0 y 1.0
        
    Ejemplo:
        >>> techs = [
        ...     Tecnologia(..., tipo="libre"),
        ...     Tecnologia(..., tipo="libre"),
        ...     Tecnologia(..., tipo="privativo"),
        ... ]
        >>> s_i = analizador.calcular_indice_soberania(techs)
        >>> s_i
        0.6666666666666666  # 2 libres de 3 total
    """
```

### Algoritmo

```python
def calcular_indice_soberania(self, tecnologias: list[Tecnologia]) -> float:
    if not tecnologias:
        return 0.0  # Sin tecnologías detectadas = sin soberanía
    
    libres = sum(1 for t in tecnologias if t.tipo == "libre")
    total = len(tecnologias)
    
    s_i = libres / total
    
    return round(s_i, 4)  # Redondear a 4 decimales
```

### Casos Edge

```python
# Si no hay tecnologías
tecnologias = []
S(i) = 0.0  ✅

# Si todas son libres
tecnologias = [libre, libre, libre]
S(i) = 1.0  ✅

# Si todas son propietarias
tecnologias = [privativo, privativo]
S(i) = 0.0  ✅

# Mezcla
tecnologias = [libre, privativo, libre, privativo, privativo]
S(i) = 2/5 = 0.4  ✅
```

---

## 🔴 MÉTODO 3: calcular_ranking_normalizado()

### Qué Hace

Convierte S(i) a ranking R(i) en escala 0-10 (más amigable para usuarios).

### Fórmula

```
R(i) = S(i) × 10

Rango: 0.0 (nada soberano) a 10.0 (totalmente soberano)

Ejemplos:
- S(i) = 0.0  → R(i) = 0.0
- S(i) = 0.5  → R(i) = 5.0
- S(i) = 1.0  → R(i) = 10.0
```

### Signature

```python
def calcular_ranking_normalizado(self, s_i: float) -> float:
    """
    Calcula ranking normalizado R(i) en escala 0-10.
    
    Args:
        s_i (float): Índice de soberanía S(i) entre 0.0 y 1.0
    
    Returns:
        float: Ranking R(i) entre 0.0 y 10.0
        
    Ejemplo:
        >>> s_i = 0.65
        >>> r_i = analizador.calcular_ranking_normalizado(s_i)
        >>> r_i
        6.5  # 0.65 × 10 = 6.5
    """
```

### Algoritmo

```python
def calcular_ranking_normalizado(self, s_i: float) -> float:
    # Validar rango
    if not (0.0 <= s_i <= 1.0):
        raise ValueError(f"S(i) debe estar entre 0.0 y 1.0, recibido: {s_i}")
    
    r_i = s_i * 10.0
    
    return round(r_i, 2)  # Redondear a 2 decimales
```

### Tabla de Referencia

```
S(i)    → R(i)   | Interpretación
───────────────────────────────────
0.0-0.2 → 0-2    | Muy baja soberanía
0.2-0.4 → 2-4    | Baja soberanía
0.4-0.6 → 4-6    | Media soberanía
0.6-0.8 → 6-8    | Buena soberanía
0.8-1.0 → 8-10   | Excelente soberanía
```

---

## 🔴 MÉTODO 4: construir_matriz_dependencia()

### Qué Hace

Crea matriz D[n×m] donde:
- Filas: instituciones analizadas (o un único análisis)
- Columnas: tecnologías detectadas
- Valores: 0 (no usa) o 1 (usa esa tecnología)

### Estructura

```python
# Ejemplo: 3 instituciones, 4 tecnologías

Matriz D:
            Google  AWS  Microsoft  Meta
Univ_A      [  1    0      1        0  ]
Univ_B      [  1    1      0        0  ]
Univ_C      [  0    0      1        1  ]

Esta matriz visualizada = Heatmap en frontend
```

### Signature

```python
def construir_matriz_dependencia(
    self, 
    tecnologias: list[Tecnologia],
    nombres_techs: list[str] = None
) -> dict:
    """
    Construye matriz de dependencia para visualización.
    
    Args:
        tecnologias (list[Tecnologia]): Techs detectadas
        nombres_techs (list[str]): Nombres de columnas (opcional)
    
    Returns:
        dict: {
            'series': [{'name': 'Institution', 'data': [0, 1, 0, 1]}, ...],
            'categories': ['Tech1', 'Tech2', 'Tech3', 'Tech4']
        }
        
    Ejemplo:
        >>> techs = [Google, AWS, Apache]
        >>> matriz = analizador.construir_matriz_dependencia(techs)
        >>> matriz['series'][0]
        {'name': 'mi_institucion', 'data': [1, 1, 0]}
    """
```

### Algoritmo

```python
def construir_matriz_dependencia(self, tecnologias: list[Tecnologia]) -> dict:
    if not tecnologias:
        return {'series': [], 'categories': []}
    
    # Nombres de tecnologías como columnas
    nombres_techs = [t.name for t in tecnologias]
    
    # Datos de esta institución
    # 1 = usa esta tech, 0 = no usa
    datos = [1 for _ in tecnologias]  # Asumiendo que todas fueron detectadas
    
    # Estructura para Apex Charts Heatmap
    return {
        'series': [
            {
                'name': 'mi_institucion',
                'data': datos
            }
        ],
        'categories': nombres_techs
    }
```

### Output Esperado

```python
{
    'series': [
        {
            'name': 'Institution 1',
            'data': [1, 1, 0, 1, 0, 1, ...]  # 18+ valores
        }
    ],
    'categories': ['Google', 'AWS', 'Microsoft', 'Meta', 'Apache', 'Linux', ...]
}
```

### Notas

- Es para Apex Charts (heatmap)
- Puede ser 1 institución o múltiples (depende de tu modelo)
- Para múltiples, anidar series:
  ```python
  'series': [
      {'name': 'Univ_A', 'data': [...]},
      {'name': 'Univ_B', 'data': [...]},
      {'name': 'Univ_C', 'data': [...]},
  ]
  ```

---

## 🔴 MÉTODO 5: generar_recomendaciones()

### Qué Hace

Genera sugerencias personalizadas basadas en S(i) y R(i).

### Signature

```python
def generar_recomendaciones(
    self,
    s_i: float,
    r_i: float,
    tecnologias: list[Tecnologia]
) -> list[str]:
    """
    Genera recomendaciones personalizadas.
    
    Args:
        s_i (float): Índice de soberanía
        r_i (float): Ranking normalizado
        tecnologias (list[Tecnologia]): Techs encontradas
    
    Returns:
        list[str]: Lista de recomendaciones en lenguaje natural
        
    Ejemplo:
        >>> s_i = 0.3
        >>> r_i = 3.0
        >>> techs = [Google, AWS, Microsoft, Apache]
        >>> recos = analizador.generar_recomendaciones(s_i, r_i, techs)
        >>> recos
        [
            'Tu institución tiene baja soberanía (30%). Considera migrar de Google Analytics.',
            'AWS es muy usado (80% dependencia). Evalúa alternativas libres.',
            'Bien: ya usas Apache (software libre).'
        ]
    """
```

### Algoritmo

```python
def generar_recomendaciones(self, s_i: float, r_i: float, tecnologias: list[Tecnologia]) -> list[str]:
    recomendaciones = []
    
    # 1. Recomendación general basada en S(i)
    if r_i < 3:
        recomendaciones.append(
            f"Tu institución tiene BAJA soberanía ({r_i:.1f}/10). "
            "Considera estrategia de migración a alternativas libres."
        )
    elif r_i < 6:
        recomendaciones.append(
            f"Soberanía MEDIA ({r_i:.1f}/10). Identifica dependencias críticas "
            "y crea plan de migración gradual."
        )
    else:
        recomendaciones.append(
            f"Excelente soberanía ({r_i:.1f}/10). Mantén esta estrategia "
            "de uso de tecnologías libres."
        )
    
    # 2. Recomendaciones específicas por tecnología
    propietarias = [t for t in tecnologias if t.tipo == "privativo"]
    
    for tech in propietarias[:3]:  # Top 3 propietarias
        recomendaciones.append(
            f"Riesgo: {tech.name} es propietaria ({tech.categoria}). "
            f"Evalúa alternativas libres (confianza: {tech.confidence:.0%})"
        )
    
    # 3. Positivo: tecnologías libres en uso
    libres = [t for t in tecnologias if t.tipo == "libre"]
    
    if libres:
        nombres_libres = ", ".join([t.name for t in libres])
        recomendaciones.append(
            f"Positivo: ya usas {len(libres)} tecnologías libres ({nombres_libres})"
        )
    
    return recomendaciones
```

### Ejemplo de Output

```python
[
    "Tu institución tiene BAJA soberanía (2.5/10). Considera estrategia de migración a alternativas libres.",
    "Riesgo: Google es propietaria (analytics). Evalúa alternativas libres (confianza: 95%)",
    "Riesgo: AWS es propietaria (hosting). Evalúa alternativas libres (confianza: 90%)",
    "Riesgo: Microsoft es propietaria (productivity). Evalúa alternativas libres (confianza: 85%)",
    "Positivo: ya usas 2 tecnologías libres (Apache, Linux)"
]
```

---

## 🧪 Testing

### Archivo: `backend_python/tests/test_api.py`

Actualiza con tests para tus métodos:

```python
import pytest
from app.analisis.analizador import AnalizadorSoberania
from app.api.modelos import Tecnologia

class TestAnalizador:
    
    @pytest.mark.asyncio
    async def test_detectar_tecnologias(self):
        """Test: detecta Google en HTML"""
        analizador = AnalizadorSoberania()
        html = "<script src='https://googleapis.com/analytics'></script>"
        
        techs = analizador.detectar_tecnologias(html)
        
        assert len(techs) > 0
        assert any(t.name == "Google" for t in techs)
    
    def test_calcular_indice_soberania(self):
        """Test: calcula S(i) correctamente"""
        analizador = AnalizadorSoberania()
        techs = [
            Tecnologia(name="Apache", tipo="libre", confidence=0.9, categoria="server"),
            Tecnologia(name="Google", tipo="privativo", confidence=0.95, categoria="analytics"),
        ]
        
        s_i = analizador.calcular_indice_soberania(techs)
        
        assert s_i == 0.5  # 1 libre de 2 total
    
    def test_calcular_ranking_normalizado(self):
        """Test: convierte S(i) a R(i)"""
        analizador = AnalizadorSoberania()
        
        r_i = analizador.calcular_ranking_normalizado(0.65)
        
        assert r_i == 6.5  # 0.65 × 10
    
    # ... más tests
```

### Ejecutar

```bash
cd backend_python
pytest tests/ -v
```

---

## 📊 Integración en Endpoints

### Dónde se llaman tus métodos

**Archivo**: `backend_python/app/api/endpoints.py`

```python
@router.post("/api/analizar", response_model=ResultadoAnalisis)
async def analizar_url(solicitud: SolicitudAnalisis):
    """
    Endpoint que usa TUS MÉTODOS
    
    Flujo:
    1. Recibe URL
    2. Llama analizador.analizar_url(url)  ← AQUÍ SE USAN TUS MÉTODOS
    3. Retorna ResultadoAnalisis JSON
    """
    
    analizador = AnalizadorSoberania()
    resultado = await analizador.analizar_url(solicitud.url)
    
    return ResultadoAnalisis(
        url=solicitud.url,
        tecnologias=resultado['tecnologias'],
        indice_soberania=resultado['s_i'],
        ranking=resultado['r_i'],
        recomendaciones=resultado['recomendaciones'],
        matriz=resultado['matriz']
    )
```

---

## 🚀 Flujo End-to-End

### Usuario accede a http://localhost:5173

```
[Frontend React]
  ↓
Usuario entra URL + click "Analizar"
  ↓
POST http://localhost:5173/api/analizar
  ↓ (Vite proxy)
  ↓
POST http://localhost:8000/api/analizar
  ↓
[Backend FastAPI]
  analizar_url(url)
    ↓
    1. Descarga HTML (YA HECHO)
    ↓
    2. Tu método: detectar_tecnologias(html)
    ↓
    3. Tu método: calcular_indice_soberania(techs)
    ↓
    4. Tu método: calcular_ranking_normalizado(s_i)
    ↓
    5. Tu método: construir_matriz_dependencia(techs)
    ↓
    6. Tu método: generar_recomendaciones(...)
    ↓
    Return: ResultadoAnalisis JSON
  ↓
[Frontend React]
  Recibe JSON
  ↓
  Renderiza gráficos con datos REALES
  ↓
Usuario ve: Dashboard con métricas
```

---

## 📦 Modelos Que Necesitas

### Ya existen en `app/api/modelos.py`

```python
# IMPORTAR ESTOS
from app.api.modelos import (
    Tecnologia,              # ← Tu detectar_tecnologias() retorna list[esto]
    SolicitudAnalisis,       # Input del endpoint
    ResultadoAnalisis,       # Output del endpoint
)

# USAR ESTOS
class Tecnologia(BaseModel):
    name: str
    tipo: str              # "privativo" o "libre"
    confidence: float      # 0.0 a 1.0
    categoria: str

class ResultadoAnalisis(BaseModel):
    url: str
    tecnologias: list[Tecnologia]
    indice_soberania: float    # S(i)
    ranking: float              # R(i)
    recomendaciones: list[str]
    matriz: dict                # Para heatmap
    # ... otros campos
```

---

## 🎯 Checklist de Implementación

### Fase 1: Preparación
- [ ] Leo este documento completamente
- [ ] Entiendo las 5 fórmulas matemáticas
- [ ] Setup del proyecto (npm install, pip install, etc)
- [ ] Veo el dashboard corriendo en http://localhost:5173

### Fase 2: Implementación
- [ ] Implemento `detectar_tecnologias()` con 18+ patrones
- [ ] Implemento `calcular_indice_soberania()`
- [ ] Implemento `calcular_ranking_normalizado()`
- [ ] Implemento `construir_matriz_dependencia()`
- [ ] Implemento `generar_recomendaciones()`

### Fase 3: Testing
- [ ] Escribo tests para cada método
- [ ] `pytest tests/ -v` pasa 100%
- [ ] Pruebo manualmente el endpoint `/api/analizar`

### Fase 4: Integración
- [ ] Pruebo end-to-end: URL → Análisis → Gráficos
- [ ] Verifica que frontend muestre datos reales
- [ ] Limpio código y agrego docstrings

### Fase 5: Entrega
- [ ] Push a rama `feature/analisis`
- [ ] PR contra `main`
- [ ] Code review con colega 1

---

## 🐛 Debugging

### Ver logs del backend en tiempo real

```bash
cd backend_python
Get-Content "logs/autonomia.log" -Wait
```

### Ver logs en consola mientras corre

```bash
python -m uvicorn main:app --port 8000 --log-level debug
```

### Probar endpoint manualmente

```bash
# PowerShell
$body = @{
    url = "https://www.example.edu.ar"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/analizar" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

## 📚 Referencias Útiles

### Dentro del Proyecto
- `ESTADO_ACTUAL.md` - Estado del proyecto
- `README.md` - Descripción general
- `ACTIVAR-DESACTIVAR.md` - Cómo correr

### Fuera del Proyecto
- Pydantic docs: https://docs.pydantic.dev/
- FastAPI docs: https://fastapi.tiangolo.com/
- Python regex: https://docs.python.org/3/library/re.html

---

## 💡 Tips

1. **Empieza simple**: Implementa detectar_tecnologias() con 5 patrones. Luego agrega más.

2. **Testing temprano**: Escribe tests mientras codificas, no después.

3. **Usa patrones robustos**: `r"googleapis\.com"` más robusto que `r"google"`

4. **Documentación**: Cada método debe tener docstring con Args, Returns, Ejemplo

5. **Preguntas**: Si algo no queda claro, pregunta (archivo tiene ejemplos para cada fórmula)

---

## 🎨 Interfaz Chat (Colega 1)

**Para el colega de UI/UX**, esto es lo que el backend le entrega:

### Input (Frontend → Backend)
```json
POST /api/analizar
{
  "url": "https://www.universidad.edu.ar"
}
```

### Output (Backend → Frontend)
```json
{
  "url": "https://www.universidad.edu.ar",
  "tecnologias": [
    {"name": "Google", "tipo": "privativo", "confidence": 0.95, "categoria": "analytics"},
    {"name": "AWS", "tipo": "privativo", "confidence": 0.90, "categoria": "hosting"},
    {"name": "Apache", "tipo": "libre", "confidence": 0.88, "categoria": "server"}
  ],
  "indice_soberania": 0.33,
  "ranking": 3.3,
  "recomendaciones": [
    "Tu institución tiene BAJA soberanía (3.3/10)...",
    "Riesgo: Google es propietaria..."
  ],
  "matriz": {
    "series": [{"name": "mi_institucion", "data": [1, 1, 1]}],
    "categories": ["Google", "AWS", "Apache"]
  }
}
```

Frontend usa esto para:
1. Mostrar animación mientras se procesa (mientras POST espera)
2. Renderizar gráficos con datos reales
3. Mostrar recomendaciones en chat

---

## 🏁 Comenzar

### Paso 1: Clone el repo (si no lo tienes)
```bash
git clone <repo_url>
cd autonomía
```

### Paso 2: Setup backend
```bash
cd backend_python
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

pip install -r requisitos.txt
```

### Paso 3: Abre el archivo donde trabajarás
```
backend_python/app/analisis/analizador.py
```

### Paso 4: Comienza con `detectar_tecnologias()`

```python
# En analizador.py, dentro de la clase AnalizadorSoberania

def detectar_tecnologias(self, html: str) -> list[Tecnologia]:
    """
    TODO: Implementar detección de tecnologías
    """
    # Aquí comienzas
    # Definir patrones, buscar en HTML, retornar lista
```

### Paso 5: Testing local
```bash
cd backend_python

# Prueba manual en Python
python
>>> from app.analisis.analizador import AnalizadorSoberania
>>> a = AnalizadorSoberania()
>>> html = "<script src='googleapis.com'></script>"
>>> techs = a.detectar_tecnologias(html)
>>> print(techs)
```

---

## 📞 Preguntas Frecuentes

**P: ¿Puedo cambiar los nombres de métodos?**
A: No, están integrados en endpoints.py. Mantén los nombres.

**P: ¿Necesito NumPy?**
A: Opcional. Para matrices complejas, instálalo: `pip install numpy`

**P: ¿Cuántas tecnologías detecto mínimo?**
A: 18+ para que sea realista. Actualmente hay 4 ejemplos, agrega 14+ más.

**P: ¿Qué confidence pongo?**
A: 0.85-0.95 para patrones seguros, 0.60-0.80 para menos seguros.

**P: ¿Puedo usar async?**
A: Sí, ya está en `analizar_url()`. Para métodos individuales: tu decisión.

---

## ✅ Éxito

Cuando termines:

1. Todos los tests pasan ✅
2. POST /api/analizar funciona ✅
3. Frontend muestra gráficos con datos reales ✅
4. PR aprobado ✅

**¡Bienvenido al equipo!** 🚀

---

**Versión**: 1.0.0-beta | **Última actualización**: Noviembre 2025
