# ❓ PREGUNTAS PARA EL EQUIPO DE BACKEND

**Imprime esto o llévalo en tu teléfono cuando hables con el backend.**

---

## 🎯 PREGUNTAS PRINCIPALES (¡IMPORTANTES!)

### 1️⃣ URL Base del Backend

**Pregunta:** 
> "¿En qué URL está corriendo el backend de FastAPI?"

**Ejemplo de respuesta esperada:**
```
http://localhost:8000
http://localhost:5000
http://mi-api.com
```

**Anota aquí:** `_________________________________`

---

### 2️⃣ Los 3 Endpoints Que Necesito

**Pregunta:** 
> "Necesito 3 endpoints (rutas) para obtener:"

#### A) Datos de la Tabla de Ranking
**Pregunta:**
> "¿Cuál es el endpoint para obtener la lista de instituciones con su índice de soberanía S(i) y ranking R(i)?"

**Ejemplo de respuesta esperada:**
```
GET /api/ranking
GET /api/instituciones
GET /api/universidades
```

**Anota aquí:** `_________________________________`

---

#### B) Datos del Gráfico de Radar
**Pregunta:**
> "¿Cuál es el endpoint para obtener la dependencia total por servicio (Google, AWS, Microsoft, Meta)?"

**Ejemplo de respuesta esperada:**
```
GET /api/dependencia-servicios
GET /api/radar
GET /api/servicios-dependencia
```

**Anota aquí:** `_________________________________`

---

#### C) Datos de la Matriz de Dependencia
**Pregunta:**
> "¿Cuál es el endpoint para obtener la matriz que muestra quién usa qué servicio?"

**Ejemplo de respuesta esperada:**
```
GET /api/matriz-dependencia
GET /api/matriz
GET /api/dependencia-matriz
```

**Anota aquí:** `_________________________________`

---

## 🔍 PREGUNTAS SOBRE EL FORMATO DE RESPUESTA

### 3️⃣ Formato JSON de Cada Endpoint

**Pregunta:** 
> "¿Puedes mostrarme un ejemplo de la respuesta JSON de cada endpoint?"

#### Respuesta esperada para `/ranking` (o similar):

```json
[
  {
    "institucion": "Universidad A",
    "s": -25,
    "r": 3.5
  },
  {
    "institucion": "Universidad B",
    "s": 67,
    "r": 8.2
  }
]
```

O podría ser:

```json
{
  "instituciones": [
    {"nombre": "Univ_A", "indice_s": -25, "ranking_r": 3.5},
    ...
  ]
}
```

**Anota la estructura aquí:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

#### Respuesta esperada para `/radar-dependencia` (o similar):

```json
{
  "servicios": ["Google", "AWS", "Microsoft", "Meta"],
  "dependencias": [2, 1, 2, 1]
}
```

O podría ser:

```json
{
  "labels": ["Google", "AWS", "Microsoft", "Meta"],
  "valores": [2, 1, 2, 1]
}
```

**Anota la estructura aquí:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

#### Respuesta esperada para `/matriz-dependencia` (o similar):

```json
{
  "instituciones": ["Univ_A", "Univ_B", "Univ_C"],
  "servicios": ["Google", "AWS", "Microsoft", "Meta"],
  "matriz": [
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1]
  ]
}
```

O podría ser:

```json
{
  "series": [
    {"name": "Univ_A", "data": [1, 0, 1, 0]},
    {"name": "Univ_B", "data": [1, 1, 0, 0]}
  ],
  "categorias": ["Google", "AWS", "Microsoft", "Meta"]
}
```

**Anota la estructura aquí:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## 🔐 PREGUNTAS DE CONFIGURACIÓN

### 4️⃣ CORS (Cross-Origin Resource Sharing)

**Pregunta:**
> "¿El backend permite peticiones HTTP desde `http://localhost:5175/`? (Es donde corre mi frontend)"

**¿Por qué pregunto?**
Si el backend no está configurado con CORS, verás un error en F12 como:
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...'
from origin 'http://localhost:5175' has been blocked by CORS policy
```

**Si hay error, dile al backend:**
> "Necesito que en FastAPI habilites CORS para `http://localhost:5175/` o para `localhost:*`"

---

### 5️⃣ Autenticación

**Pregunta:**
> "¿Los endpoints necesitan autenticación (token, API key, etc.)?"

**Si responden que sí:**
> "¿Cómo obtengo el token? ¿Es un login o algo que me dan ustedes?"

---

### 6️⃣ Puertos y URLs

**Pregunta:**
> "¿En qué puerto está corriendo el backend?"

**Respuesta esperada:**
- Puerto 8000 (FastAPI por defecto)
- Puerto 5000 (Flask por defecto)
- Otro puerto

---

## 📋 CHECKLIST DE PREGUNTAS

```
☐ 1. URL base del backend
☐ 2. Endpoint para ranking/instituciones
☐ 3. Endpoint para radar/dependencia
☐ 4. Endpoint para matriz/heatmap
☐ 5. Ejemplo JSON del endpoint 1
☐ 6. Ejemplo JSON del endpoint 2
☐ 7. Ejemplo JSON del endpoint 3
☐ 8. ¿Necesita CORS habilitado?
☐ 9. ¿Necesita autenticación?
☐ 10. ¿A qué puerto está en localhost?
```

---

## 📝 FORMULARIO RÁPIDO

**Llena esto durante la conversación:**

```
INFORMACIÓN DEL BACKEND

URL Base:
_________________________________________________________________

ENDPOINT 1 (Tabla):
Ruta: _________________________________________________
Formato JSON: ___________________________________________
Ejemplo: _______________________________________________

ENDPOINT 2 (Radar):
Ruta: _________________________________________________
Formato JSON: ___________________________________________
Ejemplo: _______________________________________________

ENDPOINT 3 (Heatmap):
Ruta: _________________________________________________
Formato JSON: ___________________________________________
Ejemplo: _______________________________________________

CONFIGURACIÓN:
¿Necesita CORS? [ ] SÍ  [ ] NO
¿Necesita autenticación? [ ] SÍ  [ ] NO
Puerto del backend: ____________________

NOTAS ADICIONALES:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## 🎙️ CÓMO HACER LAS PREGUNTAS

**Buena forma:**
> "Hola, necesito saber cuál es la URL del endpoint para obtener la lista de instituciones. ¿Qué endpoint me devuelve eso?"

**Mejor forma:**
> "Hola, estoy integrando el frontend con el backend. Necesito 3 endpoints:
> 1. Para obtener instituciones con índice S y ranking R
> 2. Para obtener dependencia por servicio (para un gráfico)
> 3. Para obtener una matriz de dependencia
> 
> ¿Cuáles son las rutas exactas y un ejemplo de respuesta JSON para cada una?"

---

## 💾 CÓMO GUARDAR LA INFORMACIÓN

**Opción 1:** Copia este documento, llénalo a mano y guárdalo

**Opción 2:** Pide al backend que te mande un documento con:
- URLs de los endpoints
- Ejemplos JSON
- Documentación OpenAPI/Swagger (si la tienen)

**Opción 3:** Pídeles que te compartan screenshots de Postman o Insomnia mostrando las respuestas

---

## 🚀 DESPUÉS DE LA CONVERSACIÓN

1. ✅ Llena el formulario
2. ✅ Actualiza `API_BASE_URL` en `src/App.jsx`
3. ✅ Actualiza los nombres de endpoints en las 3 llamadas `.get()`
4. ✅ Si el JSON es diferente, ajusta los extractores
5. ✅ Prueba en navegador y mira F12 Console

---

**¡Buena suerte con la reunión! 🚀**
