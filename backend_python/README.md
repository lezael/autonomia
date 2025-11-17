# AutonomIA - Analizador de Soberanía Tecnológica

## 📋 Descripción

AutonomIA es una aplicación web que analiza la dependencia tecnológica de instituciones mediante scraping web y álgebra matricial. Detecta tecnologías libres y privativas, genera índices de soberanía tecnológica y proporciona recomendaciones de mejora.

### MVP Características

- ✅ Análisis de dependencia tecnológica mediante scraping
- ✅ Detección de 12+ tecnologías (libres y privativas)
- ✅ Cálculo de índice de soberanía S(i)
- ✅ Ranking normalizado R(i)
- ✅ Interfaz minimalista tipo ChatGPT
- ✅ Responsive mobile-first
- ✅ Recomendaciones personalizadas

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI 0.68.0
- **Servidor**: Uvicorn 0.15.0
- **Scraping**: BeautifulSoup4 4.10.0, Requests 2.26.0
- **Análisis**: NumPy 1.21.0
- **Validación**: Pydantic 1.8.0
- **Python**: 3.8+

### Frontend
- **Lenguaje**: PHP 8.0+, HTML5, CSS3
- **JavaScript**: Vanilla JS (sin dependencias)
- **Diseño**: Mobile-first, Responsive
- **Accesibilidad**: WCAG 2.1 compliant

## 📦 Requisitos Previos

### Sistema
- Python 3.8 o superior
- PHP 8.0 o superior
- Servidor HTTP (Apache, Nginx, etc.) o PHP built-in
- pip (gestor de paquetes Python)

### Puertos Requeridos
- `8000`: Backend FastAPI (desarrollo)
- `80`: Frontend PHP (HTTP)

## 🚀 Instalación

### 1. Backend (Python)

```bash
# Navegar al directorio backend
cd backend_python

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requisitos.txt

# Iniciar servidor FastAPI
python main.py
# O usando uvicorn directamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`

### 2. Frontend (PHP)

```bash
# Opción 1: Usar PHP built-in (desarrollo)
cd frontend_php
php -S localhost:80

# Opción 2: Usar Apache o Nginx
# Configurar virtual host apuntando a frontend_php/

# Opción 3: Docker
docker run -d -p 80:80 -v $(pwd)/frontend_php:/var/www/html php:8.0-apache
```

El frontend estará disponible en: `http://localhost`

## 📁 Estructura de Directorios

```
backend_python/
├── main.py                 # Aplicación principal FastAPI
├── requisitos.txt          # Dependencias Python
├── runtime.txt             # Versión Python
└── app/
    ├── __init__.py
    ├── análisis/           # Módulo de análisis
    │   ├── calculadora_indices.py
    │   ├── constructor_matrices.py
    │   ├── normalizador_metricas.py
    │   └── operaciones_matriciales.py
    ├── api/                # Endpoints REST
    │   ├── endpoints.py
    │   ├── manejador_errores.py
    │   └── modelos_pydantic.py
    ├── extraccion/         # Detección de tecnologías
    │   ├── clasificador_tecnologias.py
    │   ├── detector_tecnologias.py
    │   ├── manejador_peticiones.py
    │   └── patrones_deteccion.py
    └── utilidades/         # Funciones comunes
        ├── auxiliares.py
        ├── logger_config.py
        └── validadores.py

frontend_php/
├── index.php               # Página principal
├── analizar.php            # Procesamiento de análisis
├── error.php               # Página de errores
├── resultados.php          # Página de resultados
├── css/
│   ├── estilos_principales.css
│   ├── componentes.css
│   └── adaptable.css
├── js/
│   ├── validaciones.js
│   ├── animaciones.js
│   └── llamadas_api.js
├── incluye/
│   ├── cabecera.php
│   ├── configuracion.php
│   └── pie_pagina.php
└── recursos/
    ├── iconos/
    └── imagenes/

documentacion/
├── API_REFERENCIA.md
├── ARQUITECTURA.md
├── ESTRUCTURA_DATOS.md
├── FLUJO_USUARIO.md
├── GUIA_DESPLIEGUE.md
└── README.md
```

## 🔌 API Endpoints

### POST /analizar
Realiza análisis de soberanía tecnológica

**Request:**
```json
{
  "url": "https://ejemplo.com"
}
```

**Response:**
```json
{
  "url": "https://ejemplo.com",
  "indice_soberania": 0.65,
  "ranking_normalizado": 0.72,
  "tecnologias_detectadas": [
    {
      "nombre": "Google Analytics",
      "tipo": "privativo",
      "confianza": 0.95,
      "categoria": "Analítica"
    }
  ],
  "tecnologias_libres_count": 2,
  "tecnologias_privativas_count": 5,
  "recomendaciones": [
    "Considerar Matomo como alternativa libre"
  ],
  "estado": "éxito",
  "mensaje": "Análisis completado exitosamente"
}
```

### GET /salud
Health check del backend

### GET /tecnologias
Lista todas las tecnologías disponibles

## 🎨 Interfaz de Usuario

### Flujo Principal
1. **Entrada**: Campo de texto grande con placeholder para URL
2. **Procesamiento**: Indicador de progreso con spinner
3. **Resultados**: Tarjetas con métricas e información
4. **Recomendaciones**: Sugerencias personalizadas

### Características de Diseño
- Tema minimalista (inspirado en ChatGPT/Claude)
- Paleta de colores clara y consistente
- Tipografía system-ui para mejor legibilidad
- Responsive: Funciona en móviles, tablets y desktop
- Dark mode optional (futuro)
- Accesibilidad: Navegación por teclado, contraste

## 🔍 Tecnologías Detectadas

### Libres (Open Source)
- Moodle
- Nextcloud
- Jitsi Meet
- BigBlueButton
- WordPress
- LibreOffice Online
- Mattermost
- Rocket.Chat

### Privativas
- Google Analytics
- Google Tag Manager
- Microsoft Azure
- AWS CloudFront
- Facebook Pixel
- LinkedIn Insight
- Google Fonts
- Salesforce
- Intercom
- Slack

## 📊 Métricas Calculadas

### Índice de Soberanía S(i)
```
S(i) = Tecnologías Libres / Total Tecnologías
Rango: 0.0 a 1.0 (0% a 100%)
```

### Ranking Normalizado R(i)
```
R(i) = S(i) normalizado a escala 0-10
Interpretación:
- 0-2: Muy bajo
- 2-4: Bajo
- 4-6: Medio
- 6-8: Alto
- 8-10: Muy alto
```

## 🔧 Configuración

### Variables de Entorno (Backend)

```bash
# En main.py o archivo .env
AMBIENTE=desarrollo  # desarrollo | producción
DEBUG=True
API_BACKEND=http://localhost:8000
LOG_LEVEL=INFO
```

### Configuración Frontend

Editar `frontend_php/js/llamadas_api.js`:

```javascript
const CONFIG_API = {
    baseURL: 'http://localhost:8000',  // URL del backend
    timeout: 30000,                     // Timeout en ms
    endpoints: {
        analizar: '/analizar',
        salud: '/salud',
        tecnologias: '/tecnologias'
    }
};
```

## 🧪 Testing

### Backend
```bash
cd backend_python
python -m pytest tests/
```

### Frontend
- Pruebas manuales en navegadores modernos
- DevTools para verificar red y console
- Validación de responsive en diferentes pantallas

## 📚 Documentación Adicional

- `documentacion/API_REFERENCIA.md` - Referencia completa de API
- `documentacion/ARQUITECTURA.md` - Arquitectura del sistema
- `documentacion/GUIA_DESPLIEGUE.md` - Guía de despliegue
- `documentacion/ESTRUCTURA_DATOS.md` - Estructura de datos
- `documentacion/FLUJO_USUARIO.md` - Flujo de usuario

## 🚢 Despliegue en Producción

### Docker

```dockerfile
# Crear archivo Dockerfile en raíz del proyecto
FROM python:3.11-slim
WORKDIR /app
COPY backend_python/requisitos.txt .
RUN pip install --no-cache-dir -r requisitos.txt
COPY backend_python .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Heroku / Cloud Platforms

```bash
# Configurar con runtime.txt
git push heroku main
```

## 🐛 Solución de Problemas

### El backend no responde
```bash
# Verificar que está corriendo
curl http://localhost:8000/salud

# Revisar logs
python main.py  # Ver output en consola
```

### CORS errors en frontend
- Verificar que FastAPI tiene CORS habilitado en main.py
- Confirmar URL del backend en `llamadas_api.js`
- Verificar headers HTTP

### Errores de timeout
- Aumentar timeout en `llamadas_api.js` (CONFIG_API.timeout)
- Verificar conexión de red
- Reducir tamaño de contenido a analizar

## 📈 Roadmap Futuro

- [ ] Matriz de dependencia visual (gráficos)
- [ ] Análisis de licencias
- [ ] Reportes descargables (PDF)
- [ ] Base de datos para histórico
- [ ] Autenticación de usuarios
- [ ] Dashboard administrativo
- [ ] API pública
- [ ] Integración CI/CD
- [ ] Modo oscuro
- [ ] Multiidioma

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## ✉️ Contacto

- **Proyecto**: AutonomIA
- **Email**: contacto@autonomia.local
- **GitHub**: [lezael/autonomia](https://github.com/lezael/autonomia)

## 🙏 Agradecimientos

- BeautifulSoup4 por parsing HTML
- FastAPI por framework moderno
- NumPy por cálculos matriciales
- Comunidad open source

---

**AutonomIA** - Analizador de Soberanía Tecnológica © 2024
