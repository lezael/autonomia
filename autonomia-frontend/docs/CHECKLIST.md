# ✅ CHECKLIST: TU PLAN DE TRABAJO FRONT-END

---

## 🎯 FASE 1: CONSTRUIR LA INTERFAZ (¡HECHO!)

**Status:** ✅ COMPLETADO

- [x] Crear estructura de carpetas
- [x] Instalar librerías (`react-chartjs-2`, `apexcharts`, `axios`)
- [x] Crear componente RadarDependencia
- [x] Crear componente TablaInstituciones
- [x] Crear componente HeatmapMatriz
- [x] Integrar todos en `App.jsx`
- [x] Probar que se ve bien en el navegador (`http://localhost:5175/`)

**Resultado:** Dashboard visual funcional con datos de ejemplo.

---

## 🚀 FASE 2: CONECTAR AL BACKEND (⏳ PRÓXIMA)

**Status:** ⏳ EN ESPERA (Necesitas info del backend)

### Subtarea 2.1: Obtener Información del Backend

- [ ] **Reunirte con el equipo de backend**
  - Matías Olivares
  - Matías Zepeda
  - Bastián Tapia

- [ ] **Preguntar las 3 URLs (endpoints) de la API**
  - URL para datos de la Tabla de Ranking
  - URL para datos del Gráfico de Radar
  - URL para datos de la Matriz de Dependencia

- [ ] **Obtener un ejemplo de respuesta JSON para cada endpoint**
  - Pide que te muestren o que te compartan screenshots/documentación

- [ ] **Anotar todos los detalles en un documento:**
  ```
  Endpoint 1: http://localhost:8000/api/???
  Formato JSON:
  {
    ...
  }
  
  Endpoint 2: http://localhost:8000/api/???
  Formato JSON:
  {
    ...
  }
  
  Endpoint 3: http://localhost:8000/api/???
  Formato JSON:
  {
    ...
  }
  ```

---

### Subtarea 2.2: Actualizar `src/App.jsx`

- [ ] Abrir `src/App.jsx`

- [ ] Cambiar la variable `API_BASE_URL` (línea ~18):
  ```javascript
  // ACTUAL
  const API_BASE_URL = 'http://localhost:8000/api';
  
  // SI EL PUERTO ES DIFERENTE, CAMBIAR A:
  const API_BASE_URL = 'http://localhost:PUERTO/ruta/api';
  ```

- [ ] Revisar que las 3 URLs de los endpoints sean correctas:
  - En `RadarDependencia`: `${API_BASE_URL}/radar-dependencia`
  - En `TablaInstituciones`: `${API_BASE_URL}/instituciones`
  - En `HeatmapMatriz`: `${API_BASE_URL}/matriz-dependencia`

- [ ] Si las URLs son diferentes, cambiarlas:
  ```javascript
  // EJEMPLO: Si la URL es /ranking en lugar de /instituciones
  axios.get(`${API_BASE_URL}/ranking`)
  ```

---

### Subtarea 2.3: Adaptar Extractores de Datos

- [ ] **Para RadarDependencia:**
  - [ ] Verificar cómo vienen los datos (JSON)
  - [ ] Si la estructura es diferente, usar `console.log()` para debuggear
  - [ ] Ajustar la forma en que se extraen `labels` y `valoresDeDependencia`

- [ ] **Para TablaInstituciones:**
  - [ ] Verificar que los campos coincidan:
    - [ ] `institucion` (o el nombre real del campo)
    - [ ] `s` (índice de soberanía)
    - [ ] `r` (ranking)
  - [ ] Si los nombres son diferentes, cambiarlos en el `.map()`

- [ ] **Para HeatmapMatriz:**
  - [ ] Verificar formato de la matriz
  - [ ] Asegurar que `series` y `categorias` se construyen correctamente

---

### Subtarea 2.4: Probar la Conexión

- [ ] Abrir navegador en `http://localhost:5175/`

- [ ] Abrir consola (F12 → Console)

- [ ] Verificar que NO hay errores de CORS o conexión

- [ ] Verificar que los gráficos se actualizan con datos reales

- [ ] Ver en consola los `console.log()` que colocaste para debuggear

**Si hay errores:**
- [ ] Anotar el error exacto
- [ ] Verificar que el backend está corriendo
- [ ] Revisar la URL en `API_BASE_URL`
- [ ] Comparar estructura JSON esperada vs recibida

---

## 🎨 FASE 3: PULIR Y FINALIZAR (DESPUÉS)

**Status:** ⏳ PENDIENTE (Después de Fase 2)

### Subtarea 3.1: Mejorar Estilos CSS

- [ ] Abrir `src/App.css`

- [ ] Mover todos los estilos en línea (`style={{...}}`) a CSS classes

- [ ] Cambiar `style={{...}}` por `className="..."` en JSX

**Ejemplo:**
```javascript
// ANTES
<div style={{ width: '600px', margin: 'auto' }}>

// DESPUÉS
<div className="radar-container">
```

```css
/* En App.css */
.radar-container {
  width: 600px;
  margin: auto;
}
```

- [ ] Asegurar que el dashboard se ve profesional

---

### Subtarea 3.2: Mejorar Manejo de Errores

- [ ] Verificar que cada componente tenga un `.catch()` en axios

- [ ] Mostrar mensajes de error amigables al usuario

- [ ] Mantener datos de ejemplo como fallback si la API falla

- [ ] Registrar errores en consola para debugging

---

### Subtarea 3.3: Añadir Interactividad (Opcional)

- [ ] (Opcional) Ordenar tabla al hacer clic en encabezados

- [ ] (Opcional) Filtrar instituciones por rango de soberanía

- [ ] (Opcional) Exportar datos a CSV

---

## 📋 RESUMEN VISUAL

```
FASE 1 ✅ → FASE 2 ⏳ → FASE 3 ⏳
```

- **Fase 1:** Interfaz lista
- **Fase 2:** Conectar datos reales (⚠️ BLOQUEADOR: Esperar al backend)
- **Fase 3:** Pulir y mejorar

---

## 🆘 PREGUNTAS PARA TU EQUIPO DE BACKEND

Prepara estas preguntas para cuando hables con el backend:

1. **"¿Cuál es la URL base del API?"**
   - Ej: `http://localhost:8000`

2. **"¿Cuáles son las 3 rutas (endpoints) para:"**
   - a) Lista de instituciones (ranking, soberanía)
   - b) Dependencia por servicio (para radar)
   - c) Matriz de dependencia (para heatmap)

3. **"¿Cuál es el formato JSON de cada respuesta?"**
   - Pide ejemplos exactos

4. **"¿Necesito configurar algo de CORS?"**
   - (Si ves error de CORS en F12)

5. **"¿A qué puerto está corriendo el backend?"**
   - (Para actualizar `API_BASE_URL`)

---

## 📍 UBICACIÓN DE ARCHIVOS IMPORTANTES

```
autonomia-frontend/
├── src/
│   ├── App.jsx              ← EDITAR AQUÍ (conexión API)
│   ├── App.css              ← EDITAR AQUÍ (estilos, Fase 3)
│   └── index.css            ← (estilos globales, si quieres)
│
├── GUIA_FRONT_END.md        ← LEE ESTO (guía completa)
├── EJEMPLOS_ADAPTACION.js   ← CONSULTA AQUÍ (ejemplos de código)
└── CHECKLIST.md             ← ERES AQUÍ (este archivo)
```

---

**¡Buena suerte! 🚀**

**Próximo paso:** Reunirte con el backend para obtener las URLs.
