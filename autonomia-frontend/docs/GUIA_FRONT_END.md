# 📋 GUÍA COMPLETA DEL FRONT-END - AUTONOMETRÍA DIGITAL

## Estado Actual

✅ **Fase 1: COMPLETADA**
- Dashboard visual funcional con 3 componentes (Radar, Tabla, Heatmap)
- Datos de ejemplo integrados
- Servidor Vite corriendo en `http://localhost:5175/`

---

## Fase 2: CONECTAR AL BACKEND (Tu Siguiente Tarea)

### 1️⃣ Paso 1: Obtener las URLs del Backend

**Reúnete con tu equipo de backend** (Matías Olivares, Matías Zepeda, Bastián Tapia) y pregunta:

> "¿Cuáles son los 3 endpoints (URLs) que necesito para obtener:"
> 1. Datos de la Tabla de Ranking (instituciones, índice S, ranking R)
> 2. Datos del Gráfico de Radar (servicios y cantidades de dependencia)
> 3. Datos de la Matriz de Dependencia (quién usa qué servicio)

**Las URLs probablemente serán algo como:**
```
GET http://localhost:8000/api/ranking
GET http://localhost:8000/api/dependencia-servicios
GET http://localhost:8000/api/matriz-dependencia
```

**Anota exactamente:**
- La URL completa de cada endpoint
- El formato JSON que devuelve (pide un ejemplo de respuesta)

---

### 2️⃣ Paso 2: Actualizar `src/App.jsx`

Una vez que tengas las URLs, reemplaza esta línea en `src/App.jsx`:

```javascript
// Línea 18 - ACTUALIZA ESTO CON LA URL DE TU BACKEND
const API_BASE_URL = 'http://localhost:8000/api';
```

Si tu backend usa puertos o URLs diferentes, cámbialo aquí.

---

### 3️⃣ Paso 3: Adaptar los Componentes

**El código ya tiene la estructura lista**, pero posiblemente necesites ajustar cómo se extrae la información del JSON devuelto por el backend.

#### Ejemplo: TablaInstituciones

Si el backend devuelve algo como:
```json
{
  "instituciones": [
    {"nombre": "Universidad A", "indice_s": -25, "ranking_r": 3.5},
    {"nombre": "Universidad B", "indice_s": 67, "ranking_r": 8.2}
  ]
}
```

Necesitarás cambiar esta línea en `TablaInstituciones`:
```javascript
// ANTES (ahora mismo)
setDatosTabla(response.data);

// DESPUÉS (ajustado a tu JSON)
setDatosTabla(response.data.instituciones);
```

Y si los nombres de las propiedades son diferentes, también ajusta esto:
```javascript
// ANTES
<td style={tdStyle}>{item.institucion}</td>

// DESPUÉS (si se llama "nombre")
<td style={tdStyle}>{item.nombre}</td>
```

---

### 4️⃣ Paso 4: Probar la Conexión

1. Asegúrate de que tu backend está corriendo en el puerto que especificaste
2. En tu navegador, ve a `http://localhost:5175/`
3. Abre la consola (F12 → Console)
4. Deberías ver mensajes como:
   - ✅ Si funciona: Los datos se cargan y los gráficos se actualizan
   - ❌ Si falla: Un error de CORS o de conexión (apunta al backend)

---

## Fase 3: PULIR Y FINALIZAR (Después)

### Mejorar los Estilos (CSS)

Los estilos ahora están "en línea" (`style={{...}}`). Para hacerlo profesional:

1. Abre `src/App.css`
2. Mueve todos los estilos allá
3. Usa `className` en lugar de `style`

**Ejemplo:**

```javascript
// ANTES (en App.jsx)
<div style={{ width: '600px', margin: 'auto' }}>

// DESPUÉS (en App.jsx)
<div className="radar-container">

// EN App.css
.radar-container {
  width: 600px;
  margin: auto;
}
```

---

### Manejo Robusto de Errores

El código ya tiene `.catch()`, pero asegúrate de que:

1. Muestre un mensaje al usuario si la API falla
2. Mantenga los datos de ejemplo como fallback
3. Registre el error en consola para debugging

---

### (Opcional) Añadir Interactividad

Ejemplo: Ordenar la tabla al hacer clic en el encabezado

```javascript
const [ordenarPor, setOrdenarPor] = useState('ranking');

const datosOrdenados = [...datosTabla].sort((a, b) => {
  if (ordenarPor === 'ranking') return b.r - a.r;
  if (ordenarPor === 'soberania') return b.s - a.s;
  return 0;
});
```

---

## 📝 Checklist de Tareas

### Fase 2 (URGENTE):
- [ ] Reunirse con backend para obtener URLs
- [ ] Obtener ejemplos JSON de respuesta
- [ ] Actualizar `API_BASE_URL` en App.jsx
- [ ] Ajustar cómo se extraen datos del JSON (si es necesario)
- [ ] Probar en navegador y verificar consola
- [ ] Confirmar que los gráficos se cargan con datos reales

### Fase 3 (Después):
- [ ] Mover estilos a `src/App.css`
- [ ] Mejorar manejo de errores
- [ ] (Opcional) Añadir interactividad

---

## 🆘 Solución de Problemas

### "Error de CORS"
→ El backend necesita permitir requests desde `http://localhost:5175/`

### "Los datos no aparecen"
→ Verifica en F12 (Console) qué URL se está llamando y qué error muestra

### "La tabla está vacía"
→ Comprueba que el JSON devuelto tiene la estructura que espera el código

---

## 📞 Información de Contacto del Backend

**Cuando necesites preguntar:**
- Matías Olivares
- Matías Zepeda
- Bastián Tapia

**Pregunta clave:**
> "¿Cuáles son los 3 endpoints REST y qué JSON devuelve cada uno?"

---

**¡Buena suerte! 🚀**
