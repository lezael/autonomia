# AutonomIA - Guía Rápida de Inicio

## 🚀 Inicio Rápido (5 minutos)

### Windows

#### 1. Iniciar Backend
```batch
iniciar_backend.bat
```
O manualmente:
```batch
cd backend_python
python -m venv venv
venv\Scripts\activate
pip install -r requisitos.txt
python main.py
```

#### 2. Iniciar Frontend (en otra terminal)
```batch
iniciar_frontend.bat
```
O manualmente:
```batch
cd frontend_php
php -S localhost:8080
```

#### 3. Acceder
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

### Linux / Mac

#### 1. Iniciar Backend
```bash
chmod +x iniciar_backend.sh
./iniciar_backend.sh
```
O manualmente:
```bash
cd backend_python
python3 -m venv venv
source venv/bin/activate
pip install -r requisitos.txt
python3 main.py
```

#### 2. Iniciar Frontend (en otra terminal)
```bash
chmod +x iniciar_frontend.sh
./iniciar_frontend.sh
```
O manualmente:
```bash
cd frontend_php
php -S localhost:8080
```

#### 3. Acceder
- **Frontend**: http://localhost:8080
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🐳 Con Docker (Recomendado para Producción)

### Requisitos
- Docker instalado
- Docker Compose

### Ejecución
```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Acceder
- **Frontend**: http://localhost
- **Backend**: http://localhost:8000
- **Proxy**: http://localhost:3000

---

## 🧪 Prueba Rápida

### 1. Verificar Backend
```bash
curl http://localhost:8000/salud
# Respuesta esperada: {"estado":"sano"}
```

### 2. Listar Tecnologías
```bash
curl http://localhost:8000/tecnologias
```

### 3. Hacer un Análisis
```bash
curl -X POST http://localhost:8000/analizar \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.google.com"}'
```

### 4. Abrir Frontend
```
http://localhost:8080
```

---

## 📋 Requisitos Previos

### Windows
- ✅ Python 3.8+ (descargable desde python.org)
- ✅ PHP 8.0+ (descargable desde php.net)
- ✅ Git (para clonar el repo)

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip python3-venv php-cli

# CentOS/RHEL
sudo yum install python3-pip python3-venv php
```

### Mac
```bash
# Con Homebrew
brew install python@3.11
brew install php
```

---

## 🔧 Configuración

### Cambiar URL del Backend (Frontend)

Editar `frontend_php/js/llamadas_api.js`:
```javascript
const CONFIG_API = {
    baseURL: 'http://tu-servidor-backend:8000',  // ← Cambiar aquí
    timeout: 30000,
    endpoints: { /* ... */ }
};
```

### Cambiar Puerto Backend

En `backend_python/main.py` (última línea):
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,  # ← Cambiar aquí (ej: 3000, 5000)
        log_level="info"
    )
```

---

## 📁 Estructura Generada

```
autonomía/
├── backend_python/
│   ├── main.py                      ← Aplicación principal
│   ├── requisitos.txt               ← Dependencias
│   ├── Dockerfile                   ← Para Docker
│   ├── README.md                    ← Documentación
│   └── app/
│       ├── api/                     ← Endpoints REST
│       ├── extraccion/              ← Detección de tech
│       ├── análisis/                ← Cálculos
│       └── utilidades/              ← Helpers
│
├── frontend_php/
│   ├── index.php                    ← Página principal
│   ├── .htaccess                    ← Configuración Apache
│   ├── css/                         ← Estilos
│   │   ├── estilos_principales.css
│   │   ├── componentes.css
│   │   └── adaptable.css
│   ├── js/                          ← Lógica
│   │   ├── llamadas_api.js
│   │   ├── validaciones.js
│   │   └── animaciones.js
│   └── incluye/                     ← Componentes PHP
│       ├── cabecera.php
│       ├── configuracion.php
│       └── pie_pagina.php
│
├── documentacion/                   ← Documentación adicional
│
├── docker-compose.yml               ← Orchestración Docker
├── iniciar_backend.bat/.sh          ← Scripts de inicio
├── iniciar_frontend.bat/.sh
└── .gitignore                       ← Archivos a ignorar
```

---

## 🐛 Solución Rápida de Problemas

### "Comando no encontrado: python"
```bash
# Windows: Añadir Python a PATH durante instalación
# O usar: python3 en lugar de python

# Linux/Mac: Instalar Python
sudo apt-get install python3-pip  # Debian/Ubuntu
brew install python@3.11           # Mac
```

### "Address already in use"
```bash
# Puerto 8000 en uso
python main.py --port 8001

# Puerto 8080 en uso (frontend)
php -S localhost:9000
```

### "CORS error" en Frontend
- Verificar que backend está corriendo en http://localhost:8000
- Revisar URL en `llamadas_api.js`
- Limpiar cache del navegador (Ctrl+Shift+Del)

### "No se conecta al backend"
```bash
# Verificar que FastAPI está corriendo
curl http://localhost:8000/salud

# Verificar firewall bloquea puerto 8000
# Windows: netstat -ano | findstr :8000
# Linux: lsof -i :8000
```

---

## 📚 Documentación Completa

Consulta estos archivos para más información:

- **`backend_python/README.md`** - Referencia técnica del backend
- **`documentacion/API_REFERENCIA.md`** - Endpoints disponibles
- **`documentacion/ARQUITECTURA.md`** - Diseño del sistema
- **`documentacion/GUIA_DESPLIEGUE.md`** - Despliegue en producción
- **`documentacion/FLUJO_USUARIO.md`** - Flujo de la aplicación

---

## ✅ Checklist de Inicio

- [ ] Python 3.8+ instalado
- [ ] PHP 8.0+ instalado
- [ ] Git clonado/descargado el repo
- [ ] Backend iniciado (`http://localhost:8000`)
- [ ] Frontend iniciado (`http://localhost:8080`)
- [ ] Ambos servicios responden correctamente
- [ ] Puedo acceder a la interfaz
- [ ] Puedo hacer una solicitud de análisis

---

## 🎯 Próximos Pasos

1. **Lee** la documentación en `documentacion/`
2. **Explora** la API en `http://localhost:8000/docs`
3. **Prueba** la interfaz en `http://localhost:8080`
4. **Modifica** configuración según necesidades
5. **Despliega** en producción con Docker

---

## 💡 Tips Útiles

### Ver logs en tiempo real
```bash
# Backend
tail -f backend_python/logs/autonomia_*.log

# Frontend PHP
php -S localhost:8080 -t frontend_php (muestra logs en consola)
```

### Resetear todo
```bash
# Eliminar entorno virtual
rm -rf backend_python/venv

# Limpiar cache del navegador
# Chrome/Firefox: Ctrl+Shift+Delete
```

### Editar en tiempo real
- Los cambios en JavaScript se reflejan al refrescar
- Los cambios en CSS se reflejan al refrescar
- Para cambios en Python, reiniciar el servidor

---

## 🆘 Soporte

Si necesitas ayuda:

1. Revisa la documentación en `documentacion/`
2. Verifica los logs en `backend_python/logs/`
3. Abre la consola del navegador (F12) para errores frontend
4. Intenta la solución de problemas arriba

---

**AutonomIA** - Analizador de Soberanía Tecnológica © 2024
