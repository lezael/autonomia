# ▶️ ACTIVAR - DESACTIVAR AutonomIA

## 🚀 INICIO RÁPIDO (TODO EN UNO)

### Windows - Command Prompt (cmd.exe)

```batch
@echo off
cd C:\Yectos\autonomía
echo.
echo ======== AUTONOMIA - INICIANDO ========
echo.
echo [1] Iniciando Backend (puerto 8000)...
start "Backend AutonomIA" cmd /k "cd backend_python && python -m venv venv & .\venv\Scripts\activate.bat & pip install -r requisitos.txt -q & python -m uvicorn main:app --port 8000"
timeout /t 3
echo.
echo [2] Iniciando Frontend (puerto 5173)...
start "Frontend AutonomIA" cmd /k "cd autonomia-frontend && npm install -q & npm run dev"
timeout /t 2
echo.
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Swagger:  http://localhost:8000/docs
echo ========================================
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause
```

**Guarda esto como**: `INICIAR.bat` en la raíz del proyecto

**Luego ejecuta**:
```batch
INICIAR.bat
```

Se abrirán 2 ventanas automáticamente:
- Terminal 1: Backend FastAPI
- Terminal 2: Frontend React

---

## 📖 INICIO MANUAL (2 Terminales)

Si prefieres hacerlo paso a paso.

### Terminal 1: Backend

```powershell
# Navegar
cd C:\Yectos\autonomía\backend_python

# Activar venv (primera vez crea venv)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias (solo primera vez)
pip install -r requisitos.txt

# Iniciar servidor
python -m uvicorn main:app --port 8000
```

**Deberías ver**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

### Terminal 2: Frontend

```powershell
# Navegar
cd C:\Yectos\autonomía\autonomia-frontend

# Instalar dependencias (solo primera vez)
npm install

# Iniciar dev server
npm run dev
```

**Deberías ver**:
```
VITE v7.2.2  ready in 253 ms
App: http://localhost:5173
```

---

## ✅ VERIFICACIÓN: ¿ESTÁ CORRIENDO?

### Backend
```
Abre: http://localhost:8000
Deberías ver: {"nombre":"AutonomIA Backend","version":"1.0.0","estado":"operacional"}
```

### Frontend
```
Abre: http://localhost:5173
Deberías ver: Dashboard con 3 gráficos (Radar, Tabla, Heatmap)
```

### API Docs
```
Abre: http://localhost:8000/docs
Swagger UI interactivo con todos los endpoints
```

---

## 🛑 DETENER TODO

### Si usaste INICIAR.bat
Cierra ambas ventanas de terminal (X en la esquina superior)

### Si lo hiciste manual
En cada terminal presiona:
```
Ctrl + C
```

Deberías ver:
```
INFO:     Shutdown complete
```

---

## 🔄 CICLO DE USO TÍPICO

### Primera Vez (Instalación)
```
TIEMPO: ~5-10 minutos

1. Ejecutar INICIAR.bat (o manual)
2. Esperar a que aparezcan ambas ventanas
3. Esperar 5-10 seg mientras instala dependencias
4. Navegar a http://localhost:5173
5. Ver dashboard cargando
```

### Usos Posteriores (Sin instalar nuevos paquetes)
```
TIEMPO: ~3-5 segundos

1. Ejecutar INICIAR.bat (o manual)
2. Esperar 3-5 seg
3. Navegar a http://localhost:5173
4. Listo
```

---

## ⚠️ PROBLEMAS COMUNES

### Error: "npm: The term 'npm' is not recognized"

**Solución**: Node.js no está en el PATH
```powershell
# En PowerShell NUEVA (no la actual)
# Cierra la terminal y abre una nueva
```

Si sigue sin funcionar:
```powershell
# Agregar Node.js manualmente
[System.Environment]::SetEnvironmentVariable(
  "Path", 
  $env:Path + ";C:\Program Files\nodejs", 
  "User"
)

# Cierra y abre PowerShell NUEVA
```

---

### Error: "Port 8000 already in use"

**Solución**: Algo ya está usando el puerto 8000
```powershell
# Buscar qué proceso usa 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Matar el proceso (reemplaza XXX con el PID)
Stop-Process -Id XXX -Force

# O usa otro puerto
python -m uvicorn main:app --port 8001
# Luego cambia Frontend: modificar vite.config.js
```

---

### Error: "venv\Scripts\Activate.ps1 cannot be loaded"

**Solución**: Política de ejecución de PowerShell restrictiva
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Responde: Y (Yes)

# Luego vuelve a ejecutar
.\venv\Scripts\Activate.ps1
```

---

### Frontend muestra "Cargando..." o "Error"

**Solución**: Backend no está corriendo
1. Verifica que Terminal 1 (Backend) muestre "Application startup complete"
2. Si no, ejecuta el comando de Backend en Terminal 1
3. Recarga navegador (F5)

---

### Error: "module not found: app"

**Solución**: Estás en la carpeta incorrecta
```powershell
# Debe ser aquí
cd C:\Yectos\autonomía\backend_python

# NO aquí
cd C:\Yectos\autonomía  # Incorrecto

# El main.py importa "from app.api...", app/ debe estar en este directorio
ls app/  # Debe listar: api, analisis, extraccion, utilidades
```

---

## 📊 ESTADO DE PUERTOS

| Puerto | Servicio | URL | Status |
|--------|----------|-----|--------|
| 5173 | Frontend React | http://localhost:5173 | ✅ |
| 8000 | Backend FastAPI | http://localhost:8000 | ✅ |
| 8000/docs | Swagger UI | http://localhost:8000/docs | ✅ |

Si cambias puertos, actualiza:
- Backend: Argumento en `uvicorn`
- Frontend: `vite.config.js` proxy target

---

## 🔗 INTEGRACIÓN FRONTEND-BACKEND

### Cómo el Frontend conecta

**Archivo**: `autonomia-frontend/src/App.jsx`

```javascript
const API_BASE_URL = '/api';  // Ruta relativa

axios.get(`${API_BASE_URL}/radar-dependencia`)
  .then(response => { /* usa datos */ })
  .catch(error => { /* manejo de error */ })
```

### Cómo funciona el proxy

**Archivo**: `autonomia-frontend/vite.config.js`

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

**Flujo**:
```
Frontend request: GET /api/radar-dependencia
       ↓
Vite intercepta (empieza con /api)
       ↓
Proxy redirige a: GET http://localhost:8000/api/radar-dependencia
       ↓
Backend responde
       ↓
Frontend recibe respuesta
```

---

## 🧹 LIMPIAR TODO

```powershell
# Borrar dependencias instaladas (libre espacio)
Remove-Item -Path "backend_python\venv" -Recurse -Force
Remove-Item -Path "autonomia-frontend\node_modules" -Recurse -Force

# Logs
Remove-Item -Path "backend_python\logs\*.log" -Force

# Re-instalar es automático al ejecutar INICIAR.bat
```

---

## 📈 MONITOREO EN TIEMPO REAL

### Ver logs del Backend
```powershell
Get-Content "backend_python\logs\autonomia.log" -Wait
# O directamente en la terminal (aparecen en vivo)
```

### Ver requests del Frontend (F12)

1. Abre navegador en http://localhost:5173
2. Presiona `F12` → Tab "Network"
3. Recarga (F5)
4. Verás todas las requests a `/api/*`

---

## 🎯 RESUMEN: PARA OCUPADO

**Quiero correr todo ahora**:
```
1. INICIAR.bat
2. http://localhost:5173
3. ¡Listo!
```

**Quiero detener**:
```
1. Cierra las 2 ventanas (X)
```

**Algo falló**:
```
Ver sección "PROBLEMAS COMUNES" arriba
O ejecutar manual (Terminal 1 + Terminal 2)
```

---

## 🛠️ Pasos de recuperación y comandos exactos (usados durante la restauración)

Estos son los comandos que se usaron para restablecer, arrancar y verificar el proyecto en mi sesión. Incluyen rutas absolutas y alternativas si `npm`/`node` no está en el PATH.

### 1) Verificar `node` / `npm` y añadir ruta temporalmente

```powershell
# Comprobar si node/npm están disponibles
node --version
npm --version

# Si PowerShell dice que npm no se reconoce, temporalmente añadir ruta (cierra/abre terminal nueva para persistir)
$env:Path = $env:Path + ";C:\Program Files\nodejs"

# Verificar de nuevo
node --version
npm --version
```

### 2) Instalar dependencias del frontend (en `autonomia-frontend`)

```powershell
cd C:\Yectos\autonomía\autonomia-frontend
npm install --no-audit --no-fund

# Si `npm` sigue sin estar disponible, usar ruta absoluta (Windows)
& 'C:\Program Files\nodejs\npm.cmd' install --no-audit --no-fund
```

### 3) Iniciar servidor de desarrollo Vite (frontend)

```powershell
# Ruta habitual
npm run dev

# Si npm no está en PATH, usar ruta absoluta a npm
& 'C:\Program Files\nodejs\npm.cmd' run dev

# Alternativa: ejecutar Vite directamente con node
& 'C:\Program Files\nodejs\node.exe' 'C:\Yectos\autonomía\autonomia-frontend\node_modules\vite\bin\vite.js' --host
```

### 4) Iniciar backend (FastAPI) desde virtualenv (recomendado)

```powershell
cd C:\Yectos\autonomía\backend_python
# Crear + activar venv (si no existe)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requisitos.txt

# Iniciar con uvicorn (modo desarrollo)
.\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000

# Para lanzar como proceso separado (no bloquear la terminal), usar Start-Process:
Start-Process -FilePath '.\venv\Scripts\python.exe' -ArgumentList @('-m','uvicorn','main:app','--host','0.0.0.0','--port','8000') -WorkingDirectory 'C:\Yectos\autonomía\backend_python'
```

### 5) Verificar salud y endpoints desde PowerShell

```powershell
# Salud general
Invoke-WebRequest -UseBasicParsing http://localhost:8000/api/salud

# Comprobación rápida de endpoints usados por la UI
foreach($ep in @('/api/radar-dependencia','/api/instituciones','/api/matriz-dependencia')) {
  Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000$ep" -TimeoutSec 5
}

# Comprobar que Vite está en http://localhost:5173
# Y que las peticiones /api/* devuelven 200 en la pestaña Network del navegador
```

### 6) Notas sobre problemas detectados y soluciones aplicadas

- Error `npm: The term 'npm' is not recognized`: solucionado temporalmente añadiendo `C:\Program Files\nodejs` al `$env:Path` y usando rutas absolutas a `npm.cmd`/`node.exe`.
- Error `ECONNREFUSED` en proxy Vite → el backend no estaba corriendo; al arrancar `uvicorn` el proxy dejó de fallar y las peticiones a `/api/*` devolvieron 200.
- Si el backend no arranca por temas de puertos, usar `Test-NetConnection -ComputerName localhost -Port 8000` y cambiar puerto si necesario.

---

**Última actualización**: Noviembre 2025 | **Versión**: 1.0.0-beta
