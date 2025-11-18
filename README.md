# 🚀 AutonomIA - Analizador de Soberanía Tecnológica

**Estado del Proyecto**: ✅ **Infraestructura Lista | Pendiente: Interfaz Chat + Análisis Matemático**

---

## 📋 Descripción General

AutonomIA es un sistema de análisis de soberanía tecnológica para instituciones de educación superior. Detecta dependencias de tecnologías propietarias y genera métricas de autonomía digital.

### 👥 Equipo de Desarrollo

| Rol | Responsable | Estado |
|-----|-------------|--------|
| **Backend Infraestructura** | Tú | ✅ Listo |
| **Frontend Visual** | Colega 1 | ✅ Listo (Dashboard gráfico) |
| **Backend Matemático** | Colega 2 | ⏳ Pendiente (Ver `COLEGA_MATEMATICO.md`) |

---

## 🏗️ Estructura del Proyecto

```
autonomía/
├── README.md                          ← Estás aquí
├── ACTIVAR-DESACTIVAR.md             ← Cómo correr y detener
├── ESTADO_ACTUAL.md                  ← Estado detallado del proyecto
├── COLEGA_MATEMATICO.md              ← Guía para tu colega
│
├── backend_python/                   ← FastAPI Backend
│   ├── main.py                       ✅ App FastAPI (puerto 8000)
│   ├── requisitos.txt                ✅ Dependencias Python
│   ├── .env.example                  ✅ Template de configuración
│   │
│   └── app/
│       ├── api/
│       │   ├── endpoints.py          ✅ 6 endpoints implementados
│       │   └── modelos.py            ✅ Schemas Pydantic
│       │
│       ├── analisis/
│       │   └── analizador.py         ⏳ TODO: Métodos para colega
│       │
│       ├── extraccion/
│       │   └── manejador_peticiones.py  ✅ Web scraping completo
│       │
│       └── utilidades/
│           └── logger_config.py      ✅ Logging configurado
│
├── autonomia-frontend/               ← React + Vite Frontend
│   ├── package.json                  ✅ Dependencias Node
│   ├── vite.config.js                ✅ Config Vite + proxy
│   ├── index.html                    ✅ Entry point
│   │
│   └── src/
│       ├── App.jsx                   ✅ Dashboard 3 gráficos
│       ├── App.css                   ✅ Estilos
│       ├── main.jsx                  ✅ Punto entrada React
│       └── index.css                 ✅ Estilos globales
│
└── .gitignore                         ✅ Git ignorados
```

---

## ⚡ Inicio Rápido

### Opción A: Manual (2 terminales)

**Terminal 1 - Backend**
```bash
cd backend_python
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate

pip install -r requisitos.txt
python -m uvicorn main:app --port 8000
```

**Terminal 2 - Frontend**
```bash
cd autonomia-frontend
npm install  # Solo la primera vez
npm run dev
```

**Resultado**
```
Frontend:   http://localhost:5173
Backend:    http://localhost:8000
Swagger UI: http://localhost:8000/docs
```

### Opción B: Con script

Ver archivo `ACTIVAR-DESACTIVAR.md` para comando todo-en-uno.

---

## 📊 Endpoints API

| Método | Endpoint | Descripción | Estado |
|--------|----------|-------------|--------|
| GET | `/` | Info API | ✅ |
| GET | `/docs` | Swagger UI | ✅ |
| GET | `/api/salud` | Health check | ✅ |
| GET | `/api/tecnologias` | Lista de 18 tech | ✅ |
| GET | `/api/radar-dependencia` | Datos gráfico radar | ✅ Ejemplo |
| GET | `/api/instituciones` | Ranking de soberanía | ✅ Ejemplo |
| GET | `/api/matriz-dependencia` | Heatmap dependencias | ✅ Ejemplo |
| POST | `/api/analizar` | **[TODO COLEGA 2]** Análisis URL | ⏳ Stub |

---

## 🎯 Próximos Pasos

### 1️⃣ Colega Diseño UI/UX (Interfaz Chat)
**Archivo**: `COLEGA_MATEMATICO.md` sección "Interfaz Chat"

**Lo que debe hacer**:
- Rediseñar frontend a interfaz tipo ChatGPT (minimalista)
- Input para ingresar URL
- Mostrar animación mientras scraping + análisis
- Transitar de chat a métricas (radar, tabla, heatmap)
- Integrar con endpoint `POST /api/analizar`

**Mantener**: Conexión a backend + estilos globales

---

### 2️⃣ Colega Matemático (Backend Análisis)
**Archivo**: `COLEGA_MATEMATICO.md`

**Lo que debe hacer**:
- Implementar 5 métodos en `app/analisis/analizador.py`:
  - `detectar_tecnologias()` → Regex patterns
  - `calcular_indice_soberania()` → Fórmula S(i)
  - `calcular_ranking_normalizado()` → Fórmula R(i)
  - `construir_matriz_dependencia()` → Matriz NumPy
  - `generar_recomendaciones()` → Sugerencias personalizadas
- Añadir patrón detector de tecnologías
- Integrar con endpoint `/api/analizar`

**Endpoints preparados**: Todo listo, solo faltan los cálculos

---

## 🔐 Seguridad & Configuración

### Variables de Entorno
```bash
# backend_python/.env (crear desde .env.example)
# Actualmente: configuración por defecto para desarrollo
```

### CORS
- Habilitado para: `localhost:5173` (frontend)
- Otros: `localhost:3000, 8000` (desarrollo)
- Producción: Cambiar en `main.py` línea ~35

### Logs
- Ubicación: `backend_python/logs/autonomia.log`
- Nivel: INFO (cambiar en `main.py` si necesario)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** 0.115.0 - Framework REST
- **Uvicorn** 0.30.0 - ASGI server
- **Pydantic** 2.9.0 - Validación schemas
- **Requests** 2.32.3 - HTTP cliente
- **BeautifulSoup4** 4.12.3 - Web scraping
- **pytest** 8.3.2 - Testing

### Frontend
- **React** 19.2.0 - UI framework
- **Vite** 7.2.2 - Build tool
- **Chart.js** + **Apex Charts** - Gráficos
- **Axios** - HTTP cliente

### Desarrollo
- **Python** 3.13+
- **Node.js** 16+
- **npm** 7+

---

## 📝 Convenciones de Código

### Python Backend
```python
# Imports ordenados: stdlib, third-party, local
from fastapi import FastAPI
from pydantic import BaseModel

from app.utilidades.logger_config import logger_app

# Funciones con docstrings
def hacer_algo():
    """Descripción breve."""
    pass
```

### React Frontend
```jsx
// Funcionales components + hooks
function ComponenteName() {
  const [state, setState] = useState(null);
  
  useEffect(() => {
    // Effects aquí
  }, []);
  
  return <div>Content</div>;
}
```

---

## 🧪 Testing

### Backend
```bash
cd backend_python
pip install pytest pytest-asyncio
pytest tests/ -v
pytest tests/ -v --cov  # Con coverage
```

### Frontend
```bash
cd autonomia-frontend
npm test
```

---

## 📚 Documentación Relacionada

- **ACTIVAR-DESACTIVAR.md** - Cómo correr/detener el proyecto
- **ESTADO_ACTUAL.md** - Estado detallado (features, endpoints, TODOs)
- **COLEGA_MATEMATICO.md** - Guía completa para el colega

---

## 🚀 Despliegue (Próximo)

Para producción:
1. Configurar `.env` con valores reales
2. Cambiar CORS en `main.py`
3. Usar `gunicorn` en lugar de `uvicorn`
4. Considerar Docker (template en `Dockerfile`)

---

## ❓ FAQ

**P: ¿Cómo agregar un nuevo endpoint?**
A: 1. Crear función en `app/api/endpoints.py` 2. Decorar con `@router.get/post()` 3. Usar models de `modelos.py`

**P: ¿Qué hace el colega matemático?**
A: Implementa los cálculos en `app/analisis/analizador.py` (ver `COLEGA_MATEMATICO.md`)

**P: ¿Puedo cambiar puertos?**
A: Backend: `python -m uvicorn main:app --port 3000` | Frontend: Vite auto-detecta

**P: ¿Cómo debuggear?**
A: Backend: `print()` en logs | Frontend: `F12` → Console

---

## 📞 Soporte

- Revisar logs: `backend_python/logs/autonomia.log`
- Backend API docs: `http://localhost:8000/docs`
- Issues: Crear en repositorio

---

**Última actualización**: Noviembre 2025 | **Versión**: 1.0.0-beta
