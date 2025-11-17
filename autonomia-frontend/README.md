# Dashboard de Autonometría Digital

Análisis de Soberanía Tecnológica en Instituciones de Educación Superior.

## 🚀 Inicio Rápido

### Requisitos Previos
- Node.js 18+ y npm
- Python 3.10+

### Instalación y Ejecución

**1. Instalar dependencias del frontend:**
```bash
npm install
```

**2. Iniciar el servidor de desarrollo frontend:**
```bash
npm run dev
```
Abre [http://localhost:5173](http://localhost:5173) en tu navegador.

**3. Iniciar el backend (en otra terminal):**
```bash
cd ../autonomia/backend_python
python -m uvicorn main:app --reload
```
El backend estará en [http://localhost:8000](http://localhost:8000)

## 📁 Estructura del Proyecto

```
autonomia-frontend/
├── src/
│   ├── App.jsx          # Componente principal con 3 visualizaciones
│   ├── App.css          # Estilos profesionales
│   ├── index.css        # Estilos globales
│   └── main.jsx         # Punto de entrada
├── docs/                # Documentación completa del proyecto
├── public/              # Assets estáticos
├── package.json         # Dependencias npm
└── vite.config.js       # Configuración Vite + proxy
```

## 🎨 Características

- ✅ **Gráfico Radar**: Dependencia total por servicio
- ✅ **Tabla Ranking**: Instituciones ordenadas por índice de soberanía
- ✅ **Heatmap**: Matriz de dependencia institución-servicio
- ✅ **Diseño Responsive**: Adaptado a móviles y tablets
- ✅ **Estados de Carga**: Indicadores visuales de carga/error
- ✅ **Conexión API**: Proxy Vite configurado para evitar CORS

## 📚 Documentación

Toda la documentación está en la carpeta `/docs`:
- `GUIA_FRONT_END.md` - Guía completa del frontend
- `CORS_PARA_BACKEND.md` - Configuración CORS para backend
- `INDICE_MAESTRO.md` - Índice de toda la documentación
- Y 14 documentos más...

## 🔧 Tecnologías

- **Frontend**: React 19 + Vite 7.2
- **Gráficos**: Chart.js, ApexCharts
- **HTTP Client**: Axios
- **Backend**: FastAPI + Uvicorn
- **Estilos**: CSS3 con variables y animaciones

## 📊 Endpoints de la API

- `GET /api/radar-dependencia` - Datos para gráfico radar
- `GET /api/instituciones` - Lista de instituciones con índices
- `GET /api/matriz-dependencia` - Matriz para heatmap

## 🛠️ Scripts Disponibles

```bash
npm run dev      # Desarrollo con hot reload
npm run build    # Build para producción
npm run preview  # Preview del build de producción
npm run lint     # Ejecutar ESLint
```

## 🎯 Estado del Proyecto

✅ Fase 1: Interfaz UI - **Completado**  
✅ Fase 2: Backend integrado - **Completado**  
✅ Fase 3: Diseño profesional - **Completado**

---

**Desarrollado con ❤️ para el análisis de Autonometría Digital**
