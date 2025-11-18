# 🎯 REFERENCIA RÁPIDA - AutonomIA

**Use this as a quick lookup** | Bookmarks para los tres roles

---

## 👤 Para Ti (Backend Infraestructura)

### Links Rápidos
- **Código**: `backend_python/main.py` + `backend_python/app/api/endpoints.py`
- **Tests**: `backend_python/tests/test_api.py`
- **Guía Colega**: `COLEGA_MATEMATICO.md`
- **Estado**: `ESTADO_ACTUAL.md`

### Comandos Útiles
```bash
# Iniciar todo
INICIAR.bat

# Backend solo
cd backend_python
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --port 8000

# Tests
cd backend_python
pytest tests/ -v

# Ver logs
Get-Content "backend_python\logs\autonomia.log" -Wait

# API docs
http://localhost:8000/docs
```

### Checklist
- [x] Infraestructura backend ✅
- [x] Endpoints setup ✅
- [x] CORS configurado ✅
- [x] Web scraping listo ✅
- [x] Logging centralizado ✅
- [x] Tests scaffold ✅
- [ ] Esperar colega 2 (análisis)
- [ ] Code review PR colega 2

---

## 👨‍🎨 Para Colega 1 (UI/UX - Interfaz Chat)

### Links Rápidos
- **Código**: `autonomia-frontend/src/App.jsx`
- **Config Vite**: `autonomia-frontend/vite.config.js`
- **Guía**: Ver sección "Interfaz Chat" en `COLEGA_MATEMATICO.md`
- **Estado**: `ESTADO_ACTUAL.md`

### Comandos Útiles
```bash
# Iniciar frontend
INICIAR.bat

# Frontend solo
cd autonomia-frontend
npm run dev

# Ver en navegador
http://localhost:5173

# DevTools
F12 en navegador
```

### Lo que necesitas saber
- Backend envía JSON con: `indice_soberania`, `ranking`, `tecnologias`, `recomendaciones`, `matriz`
- Tú rediseñas interfaz a ChatGPT-style
- Mantén conexión a `/api/analizar`
- Input: URL, Output: Métricas gráficas

### Checklist
- [ ] Interfaz minimalista (chat-style)
- [ ] Input URL + botón enviar
- [ ] Animación scraping
- [ ] Animación análisis
- [ ] Transición a gráficos
- [ ] Integración /api/analizar
- [ ] Testing end-to-end
- [ ] PR a main

---

## 🧮 Para Colega 2 (Análisis Matemático)

### Links Rápidos
- **GUÍA COMPLETA**: `COLEGA_MATEMATICO.md` ← LEE ESTO PRIMERO
- **Código a editar**: `backend_python/app/analisis/analizador.py`
- **Tests a escribir**: `backend_python/tests/test_api.py`
- **Referencia APIs**: `backend_python/app/api/endpoints.py` + `modelos.py`

### Comandos Útiles
```bash
# Setup
cd backend_python
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requisitos.txt

# Iniciar backend
python -m uvicorn main:app --port 8000

# Tests
pytest tests/ -v

# Python REPL para testing
python
>>> from app.analisis.analizador import AnalizadorSoberania
>>> a = AnalizadorSoberania()
>>> # test tus métodos aquí
```

### Métodos a Implementar
```python
1. detectar_tecnologias(html)      → list[Tecnologia]
2. calcular_indice_soberania()     → float (0-1)
3. calcular_ranking_normalizado()  → float (0-10)
4. construir_matriz_dependencia()  → dict (Apex Charts format)
5. generar_recomendaciones()       → list[str]
```

### Checklist
- [ ] Leo COLEGA_MATEMATICO.md
- [ ] Setup backend + venv
- [ ] Ejecuto INICIAR.bat
- [ ] Implemento detectar_tecnologias()
- [ ] Implemento calcular_indice_soberania()
- [ ] Implemento calcular_ranking_normalizado()
- [ ] Implemento construir_matriz_dependencia()
- [ ] Implemento generar_recomendaciones()
- [ ] Escribo tests para cada método
- [ ] pytest tests/ -v pasa 100%
- [ ] Pruebo endpoint /api/analizar manualmente
- [ ] PR a feature/analisis
- [ ] Code review aprobado

---

## 🌐 URLs Importantes

| URL | Qué es | Cuándo usarlo |
|-----|--------|--------------|
| http://localhost:8000 | Backend API | Testing backend |
| http://localhost:8000/docs | Swagger UI | Ver/probar endpoints |
| http://localhost:5173 | Frontend Dashboard | Ver UI |
| http://localhost:5173/?debug | Debug mode | Troubleshooting |

---

## 📊 API Endpoints

```
GET  /                          → Info API
GET  /docs                      → Swagger UI
GET  /api/salud                 → Health check
GET  /api/tecnologias           → List 18 techs
GET  /api/radar-dependencia     → Radar data
GET  /api/instituciones         → Institutions table
GET  /api/matriz-dependencia    → Heatmap matrix
POST /api/analizar              → Main analysis (TODO: colega 2)
```

---

## 🔧 Troubleshooting Rápido

### "Port 8000 already in use"
```bash
# Find process using 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Kill it
Stop-Process -Id <PID> -Force

# Or use different port
python -m uvicorn main:app --port 8001
```

### "npm: The term 'npm' is not recognized"
```powershell
# Reinicia PowerShell NUEVA (cerrando la actual)
# Node.js necesita ser en nueva sesión

# O agrega Node al PATH manualmente
[System.Environment]::SetEnvironmentVariable(
  "Path", 
  $env:Path + ";C:\Program Files\nodejs", 
  "User"
)
```

### "Frontend shows Error / Backend not responding"
```
Checklist:
1. ¿Backend terminal muestra "Application startup complete"?
2. ¿http://localhost:8000 responde en navegador?
3. ¿Frontend console (F12) muestra CORS errors?

Solución:
- Terminal 1: Ctrl+C para matar backend
- Terminal 1: python -m uvicorn main:app --port 8000
- Terminal 2: npm run dev
- Recargar navegador (F5)
```

### "pytest: command not found"
```bash
cd backend_python
.\venv\Scripts\Activate.ps1
pip install pytest pytest-asyncio
pytest tests/ -v
```

---

## 📚 Documentación Matriz

| Para... | Lee esto | Tiempo |
|---------|----------|--------|
| Entender proyecto | README.md | 5 min |
| Correr todo | ACTIVAR-DESACTIVAR.md | 5 min |
| Ver progreso | ESTADO_ACTUAL.md | 10 min |
| **COLEGA 2**: Implementar | COLEGA_MATEMATICO.md | 30 min |
| Pre-commit check | PARA_REPOSITORIO.md | 5 min |
| Referencia rápida | ESTA PÁGINA | 2 min |

---

## 🚀 Primer Día Checklist

### Paso 1: Setup (5 min)
- [ ] Clone repo / ya tengo acceso
- [ ] Leo README.md
- [ ] Leo documentación de mi rol

### Paso 2: First Run (5 min)
```bash
INICIAR.bat
# Espera que se abran 2 ventanas
# Abre http://localhost:5173
# Verifica dashboard carga
```

### Paso 3: Conocer el código (20 min)
- Backend: Lee `main.py` + `app/api/endpoints.py`
- Frontend: Lee `autonomia-frontend/src/App.jsx`
- Tests: Abre `tests/test_api.py`

### Paso 4: Hacer cambio pequeño (15 min)
- Backend: Agrega print() en un endpoint, verifica en logs
- Frontend: Cambia color de un elemento, verifica HMR
- Matemático: Agrega método de prueba, verifica pytest

### Paso 5: Entender integración (10 min)
- Abre DevTools (F12)
- Mira Network tab mientras Frontend hace requests
- Ve cómo el Backend responde en Terminal 1

---

## 💾 Git Workflow

### Branch Strategy
```
main (stable)
├── feature/analisis          ← Colega 2
├── feature/chat-interface    ← Colega 1
└── bugfix/[issue]            ← Any fixes
```

### Commit Message Format
```
feat: Descripción de feature
fix: Descripción del fix
docs: Cambios en documentación
test: Cambios en tests
refactor: Refactorización

Ejemplo:
feat: Implementar detectar_tecnologias con 18 patrones

- Agrega función detectar_tecnologias en analizador.py
- Cubre Google, AWS, Microsoft, Meta, Apache, Linux, etc
- Tests en test_api.py con 95% coverage
- Integración en /api/analizar endpoint
```

### Push & PR
```bash
git checkout -b feature/[nombre]
# Do work
git add .
git commit -m "feat: ..."
git push origin feature/[nombre]
# Abre PR en GitHub
```

---

## 🎯 Success Criteria

### Backend
- [x] FastAPI runs on port 8000 ✅
- [x] CORS configured for localhost:5173 ✅
- [x] 6 endpoints responding ✅
- [ ] Analysis endpoint complete (colega 2)
- [ ] 100% test coverage (colega 2)

### Frontend
- [x] React + Vite on port 5173 ✅
- [x] 3 gráficos rendering ✅
- [x] Proxy to backend working ✅
- [ ] Chat-style interface (colega 1)
- [ ] Smooth animations (colega 1)

### Analysis
- [ ] All 5 methods implemented (colega 2)
- [ ] All tests passing (colega 2)
- [ ] 18+ technologies detected (colega 2)
- [ ] Metrics displayed in UI (colega 1 + 2)

---

## 📞 Support Quick Links

- **Swagger API Docs**: http://localhost:8000/docs
- **Backend Logs**: `backend_python/logs/autonomia.log`
- **Frontend Console**: F12 en navegador
- **Code**: Read docstrings (todas las funciones las tienen)

---

## 🎉 Versión

**AutonomIA**: 1.0.0-beta  
**Última actualización**: Noviembre 2025  
**Estado**: ✅ Infraestructura Lista | ⏳ Análisis Pendiente

---

**Bookmark esta página para referencia rápida** 🔖
