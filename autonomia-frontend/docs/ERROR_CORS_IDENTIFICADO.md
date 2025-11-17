# 🚨 IDENTIFICADO: ERROR DE CORS

**Fecha:** 15 de noviembre de 2025  
**Estado:** Identificado y documentado  
**Prioridad:** 🔴 CRÍTICA

---

## ¿QUÉ VISTE?

En tu navegador (F12 → Console) probablemente viste un mensaje como:

```
Access to XMLHttpRequest at 'http://localhost:8000/api/instituciones'
from origin 'http://localhost:5173' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

O en naranja:
```
⚠️ Error: Network Error
Mostrando datos de ejemplo
```

---

## ¿QUÉ SIGNIFICA?

**CORS** = Cross-Origin Resource Sharing

El navegador está **bloqueando** la petición porque:

```
Frontend (React)         Backend (FastAPI)
http://localhost:5173/   vs   http://localhost:8000/
     ↓
   "Son orígenes diferentes"
     ↓
   "¡Bloqueado por seguridad!"
```

Por defecto, los navegadores no permiten que una página web acceda a datos de otro "origen" (dominio + puerto).

---

## ¿QUIÉN TIENE QUE ARREGLARLO?

**Respuesta: Tu equipo de BACKEND**

No es un problema de tu código React. Es una configuración que falta en FastAPI.

---

## ¿QUÉ TIENE QUE HACER EL BACKEND?

Tu equipo necesita agregar **CORS Middleware** a su FastAPI.

**Archivo a modificar:** `main.py` (o como le hayan llamado)

**Lo que deben hacer:**

1. Abrir su archivo `main.py`
2. Copiar el código de `CORS_PARA_BACKEND.md`
3. Pegarlo en su proyecto
4. Reiniciar el servidor

**Tiempo:** 5 minutos

---

## TÚ PUEDES HACER ESTO MIENTRAS ESPERAS

### 1. Crear una versión mejorada de tu código

Hemos creado `src/App_MEJORADO.jsx` con:
- ✅ Mejor visualización de estado "Cargando"
- ✅ Mejores mensajes de error
- ✅ Logging mejorado en consola

**Para usar la versión mejorada:**

```bash
# 1. Renombra tu actual
mv src/App.jsx src/App_VIEJO.jsx

# 2. Renombra la mejorada
mv src/App_MEJORADO.jsx src/App.jsx

# 3. Recarga el navegador
# El dashboard debería verse igual, pero con mejores mensajes
```

---

## PASOS A SEGUIR

### PASO 1: Prepara la documentación para el backend

1. Abre `CORS_PARA_BACKEND.md`
2. Imprime o cópialo
3. Entrégalo a tu equipo de backend

### PASO 2: Ellos agregan CORS (5 min)

El backend agrega 10 líneas de código:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### PASO 3: Reinician el servidor

```bash
# Ctrl+C para detener
# Luego:
uvicorn main:app --reload
```

### PASO 4: Prueba en tu navegador

Recarga la página. El error debería desaparecer.

---

## MIENTRAS ESPERAS AL BACKEND

Puedes hacer esto:

### ✅ Opción 1: Usar la versión mejorada del código

```bash
# Reemplaza tu App.jsx con App_MEJORADO.jsx
# Tendrás mejores mensajes y logging
```

### ✅ Opción 2: Verificar que el backend responde

```bash
# En tu navegador, ve a:
http://localhost:8000/

# Si ves algo → El servidor está corriendo ✅
# Si ves "No se puede acceder" → El servidor no está corriendo ❌
```

### ✅ Opción 3: Revisar la consola (F12)

```bash
# Abre F12 en tu navegador
# Consola → Busca mensajes 📡 y ✅ y ❌
# Sabrás exactamente qué endpoint está intentando conectar
```

---

## CHECKLIST: TÚ

```
☐ Leí este documento
☐ Entiendo que es un error de CORS
☐ Sé que lo tiene que arreglar el backend
☐ Tengo listo CORS_PARA_BACKEND.md para entregarle al backend
☐ (Opcional) Usé App_MEJORADO.jsx para mejor UX
☐ (Opcional) Verifiqué que el backend responde en localhost:8000
```

---

## CHECKLIST: BACKEND

Pasa esto al backend:

```
☐ Leer CORS_PARA_BACKEND.md
☐ Copiar el código de CORS
☐ Pegarlo en main.py
☐ Guardar el archivo
☐ Reiniciar uvicorn (Ctrl+C y volver a iniciar)
☐ Verificar que el error de CORS desaparece
☐ Avisar al frontend que está listo
```

---

## ¿QUÉ PASARÁ CUANDO ARREGLEN CORS?

Una vez que el backend agregue CORS:

1. ❌ El error desaparecerá
2. ✅ Los datos se cargarán desde la API
3. ✅ Los gráficos se actualizarán con datos reales
4. ✅ **¡La aplicación funcionará completamente!**

---

## REFERENCIA RÁPIDA

| Problema | Causa | Solución |
|----------|-------|----------|
| Error de CORS | Backend no permite tu localhost | Backend agrega CORS Middleware |
| "Cannot GET /api/..." | Endpoint no existe | Verificar nombre del endpoint |
| Datos vacíos | Estructura JSON diferente | Adaptar extractores de datos |
| "Cannot connect" | Backend no está corriendo | Iniciar uvicorn |

---

## 📞 CONTACTO

**Si necesitas ayuda:**

### Para el Frontend:
- Usa: `DEBUG_SCRIPT.js` (en F12 Console)
- Lee: `GUIA_FRONT_END.md`
- Consulta: `MAPA_RAPIDO.md`

### Para el Backend:
- Usa: `CORS_PARA_BACKEND.md` (esta es la guía)
- Pregunta: ¿Necesito hacer algo más?

---

## 🎯 PRÓXIMOS PASOS

### Ahora (Hoy):
1. Entrega `CORS_PARA_BACKEND.md` al backend
2. (Opcional) Usa `App_MEJORADO.jsx`

### Mañana (Cuando backend agregue CORS):
1. Recarga navegador
2. ¡Debería funcionar!
3. Si no funciona → Revisa `DEBUG_SCRIPT.js`

---

## ✨ RESUMEN

```
El problema: Error de CORS
La causa: Backend no permite tu localhost
La solución: Backend agrega 10 líneas de código
Tiempo para arreglarlo: 5 minutos
Quién lo arregla: El backend
Tú mientras: Esperas o mejoras tu código
```

---

**Documento de Identificación de Error**  
**CORS - Autonometría Digital**  
**15 de noviembre de 2025**
