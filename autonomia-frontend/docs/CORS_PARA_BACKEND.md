# 🔌 GUÍA DE CORS PARA EL BACKEND

**Para:** Matías Olivares, Matías Zepeda, Bastián Tapia (Equipo Backend)  
**De:** Frontend  
**Urgencia:** 🔴 CRÍTICA - Sin esto, el frontend no puede acceder a los datos

---

## ⚠️ EL PROBLEMA

El frontend (React) en `http://localhost:5173/` está intentando conectarse a la API en `http://localhost:8000/`, pero el navegador bloquea la petición por **Error de CORS**.

**Mensaje que se ve en la consola del navegador:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

---

## ✅ LA SOLUCIÓN

Necesitan agregar **CORS Middleware** a su aplicación FastAPI.

### Paso 1: Copiar este código

Copien **EXACTAMENTE** este código:

```python
# En su archivo principal (ej. main.py)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← AGREGAR ESTA IMPORTACIÓN

app = FastAPI()

# ← AGREGAR ESTO (la configuración de CORS)
origins = [
    "http://localhost:5173",      # Frontend de React
    "http://127.0.0.1:5173",      # Alternative localhost
    "http://localhost",            # Sin puerto
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Solo estos orígenes tienen permiso
    allow_credentials=True,        # Permitir cookies/autenticación
    allow_methods=["*"],           # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],           # Todos los headers
)

# ← DESPUÉS DE ESTO SIGUE EL RESTO DE SU CÓDIGO NORMALMENTE
# @app.get("/api/ranking")
# def get_ranking():
#     ...
```

### Paso 2: Guardar y reiniciar

1. Guarden el archivo `main.py`
2. **Detengan** el servidor FastAPI (Ctrl+C en la terminal)
3. **Reinicien** el servidor:
   ```bash
   uvicorn main:app --reload
   ```

### Paso 3: Verificar

1. Frontend debería dejar de mostrar errores de CORS
2. Si los datos aún no aparecen, el problema es otro (ver sección "Si aún falla")

---

## 🔍 SI AÚN FALLA

Hagan esto para debuggear:

### Test 1: ¿El servidor está corriendo?
```bash
# Desde la terminal del backend
# Deberían ver algo como:
# Uvicorn running on http://127.0.0.1:8000
# Si no lo ven, inicien el servidor
```

### Test 2: ¿La API responde?
```bash
# Abre Chrome y ve a:
# http://localhost:8000/api/instituciones
# (o el endpoint que hayan creado)

# Si ves JSON → El servidor funciona ✅
# Si ves "Cannot GET" → El endpoint no existe ❌
# Si ves "Cannot connect" → El servidor no está corriendo ❌
```

### Test 3: ¿CORS está configurado?
```bash
# El navegador debería DEJAR DE mostrar:
# "has been blocked by CORS policy"

# Si sigue mostrando, significa que:
# 1. El código de CORS no se guardó bien
# 2. El servidor no se reinició después de guardar
# 3. El frontend sigue apuntando a un puerto diferente
```

---

## 📝 DETALLES IMPORTANTES

### ¿Qué es CORS?
CORS = "Cross-Origin Resource Sharing"  
Significa: "Permitir que otros sitios accedan a mis datos"

Por defecto, FastAPI **NO permite** que otros orígenes accedan a sus datos.

El código que copiaron arriba le dice a FastAPI:
> "Oye, permite que `http://localhost:5173/` acceda a todos mis endpoints"

### ¿Por qué necesitamos esto?
- Frontend corre en `http://localhost:5173/` ← Un origen
- Backend corre en `http://localhost:8000/` ← Otro origen
- El navegador lo ve como "inseguro" y bloquea
- CORS dice "está bien, son la misma aplicación"

### ¿Qué es `allow_origins`?
```python
origins = [
    "http://localhost:5173",  # ← El frontend
]
```

Es una lista de orígenes que tienen permiso.

**En desarrollo** pueden poner:
```python
origins = ["*"]  # Permite TODOS (pero no para producción)
```

**En producción** deben ser específicos:
```python
origins = ["https://mi-dominio.com"]
```

---

## ✨ EJEMPLO COMPLETO

Si su `main.py` se ve así **ANTES**:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/ranking")
def get_ranking():
    return [{"institucion": "Univ_A", "s": -25, "r": 3.5}]
```

Debería verse así **DESPUÉS**:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← NUEVA IMPORTACIÓN

app = FastAPI()

# ← NUEVO CÓDIGO CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ← FIN NUEVO CÓDIGO

@app.get("/api/ranking")
def get_ranking():
    return [{"institucion": "Univ_A", "s": -25, "r": 3.5}]
```

---

## 🆘 CHECKLIST RÁPIDA

```
☐ ¿Copiaron el código de CORS en main.py?
☐ ¿El archivo se guardó?
☐ ¿Reiniciaron el servidor uvicorn?
☐ ¿El frontend en navegador YA NO muestra error de CORS?
☐ ¿El servidor responde en http://localhost:8000/api/...?
☐ ¿Los datos aparecen ahora en el frontend?
```

---

## 📞 SI NECESITAN AYUDA

Envíen un screenshot de:
1. La terminal donde corre `uvicorn` (mostrar que está corriendo)
2. La consola del navegador (F12 → Console) mostrando el error
3. El archivo `main.py` (para verificar que CORS está bien)

---

## 🎯 EL OBJETIVO

Una vez hagan esto:
1. El error de CORS desaparecerá
2. El frontend podrá conectarse a la API
3. Los gráficos se actualizarán con datos reales
4. **¡La aplicación funcionará completamente!**

---

## 📌 RESUMEN

**Hacer en el backend (FastAPI):**
```
1. Copiar el código de CORS
2. Pegarlo en main.py (después del app = FastAPI())
3. Guardar
4. Reiniciar el servidor
5. Verificar que el error desaparezca
```

**Tiempo estimado:** 5 minutos  
**Dificultad:** ⭐ Muy fácil

---

**Una vez hagan esto, avísame y verificaremos que todo funciona correctamente.**

---

*Guía CORS para Backend - Autonometría Digital*  
*Generada: 15 de noviembre de 2025*
