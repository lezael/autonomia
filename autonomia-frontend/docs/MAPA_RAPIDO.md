# 🗺️ MAPA RÁPIDO - ¿DÓNDE EDITAR QUÉ?

Use este documento como referencia rápida para saber exactamente dónde hacer cambios.

---

## 📍 TAREA: Cambiar la URL del Backend

**Archivo:** `src/App.jsx`  
**Línea:** ~18

```javascript
// ANTES
const API_BASE_URL = 'http://localhost:8000/api';

// DESPUÉS (Reemplaza con la URL correcta)
const API_BASE_URL = 'http://tu-backend.com/api';
```

---

## 📍 TAREA: Cambiar el nombre de un endpoint

**Archivo:** `src/App.jsx`

### Para la Tabla:
**Línea:** ~100

```javascript
// ANTES
axios.get(`${API_BASE_URL}/instituciones`)

// DESPUÉS (Si el endpoint es diferente)
axios.get(`${API_BASE_URL}/ranking`)
// O
axios.get(`${API_BASE_URL}/universidades`)
```

### Para el Radar:
**Línea:** ~70

```javascript
// ANTES
axios.get(`${API_BASE_URL}/radar-dependencia`)

// DESPUÉS (Si el endpoint es diferente)
axios.get(`${API_BASE_URL}/dependencia-servicios`)
```

### Para el Heatmap:
**Línea:** ~145

```javascript
// ANTES
axios.get(`${API_BASE_URL}/matriz-dependencia`)

// DESPUÉS (Si el endpoint es diferente)
axios.get(`${API_BASE_URL}/matriz`)
```

---

## 📍 TAREA: Adaptar cómo se extraen los datos

**Archivo:** `src/App.jsx`

### Si el JSON viene anidado en un campo:

**Para TablaInstituciones (Línea ~103):**

```javascript
// ANTES
.then((response) => {
  setDatosTabla(response.data);

// DESPUÉS (Si el backend devuelve: { instituciones: [...] })
.then((response) => {
  setDatosTabla(response.data.instituciones);
  // O si está más anidado: response.data.data.items
```

**Para RadarDependencia (Línea ~73):**

```javascript
// ANTES
.then((response) => {
  setDatosRadar(response.data);

// DESPUÉS (Si el backend devuelve estructura diferente)
.then((response) => {
  setDatosRadar({
    labels: response.data.servicios,
    valoresDeDependencia: response.data.dependencias,
  });
```

**Para HeatmapMatriz (Línea ~150):**

```javascript
// ANTES
.then((response) => {
  setDatosHeatmap(response.data);

// DESPUÉS (Si necesitas procesar la matriz)
.then((response) => {
  const series = response.data.instituciones.map((inst, idx) => ({
    name: inst,
    data: response.data.matriz[idx],
  }));
  setDatosHeatmap({
    series: series,
    categorias: response.data.servicios,
  });
```

---

## 📍 TAREA: Cambiar los nombres de las columnas de la tabla

**Archivo:** `src/App.jsx`  
**Línea:** ~117-120

```javascript
// ANTES
<tr key={item.institucion}>
  <td style={tdStyle}>{item.institucion}</td>
  <td style={tdStyle}>{item.s}</td>
  <td style={tdStyle}>{item.r}</td>

// DESPUÉS (Si los campos se llaman diferente)
<tr key={item.id}>
  <td style={tdStyle}>{item.nombre}</td>
  <td style={tdStyle}>{item.indice_soberania}</td>
  <td style={tdStyle}>{item.ranking}</td>
```

---

## 📍 TAREA: Mejorar los estilos (Fase 3)

**Archivo para LEER:** `src/App.jsx`  
**Archivo para ESCRIBIR:** `src/App.css`

**Paso 1:** Identifica todos los `style={{...}}` en App.jsx

**Paso 2:** Cópialos a App.css como clases CSS

**Ejemplo:**

```javascript
// EN App.jsx AHORA:
<div style={{ width: '600px', margin: 'auto' }}>

// CAMBIA A:
<div className="radar-container">
```

```css
/* EN App.css AGREGA: */
.radar-container {
  width: 600px;
  margin: auto;
}
```

---

## 📍 TAREA: Mejorar manejo de errores

**Archivo:** `src/App.jsx`

Los componentes ya tienen `.catch()`, pero puedes mejorar el mensaje:

```javascript
// ANTES
.catch((error) => {
  console.error('Error al traer datos del Radar:', error);
  setErrorRadar('No se pudieron cargar los datos del Radar');
  setCargandoRadar(false);
});

// DESPUÉS (Mensaje más específico)
.catch((error) => {
  console.error('Error en /radar-dependencia:', error);
  if (error.response?.status === 404) {
    setErrorRadar('Endpoint no encontrado. Verifica la URL.');
  } else if (error.code === 'ECONNREFUSED') {
    setErrorRadar('No se puede conectar al backend. ¿Está corriendo?');
  } else {
    setErrorRadar('Error al cargar datos: ' + error.message);
  }
  setCargandoRadar(false);
});
```

---

## 📍 TAREA: Agregar una columna a la tabla

**Archivo:** `src/App.jsx`

### Paso 1: Agregar encabezado

**Línea:** ~111

```javascript
// ANTES
<th style={thStyle}>Institución</th>
<th style={thStyle}>Índice S(i) (%)</th>
<th style={thStyle}>Ranking R(i) (0-10)</th>

// DESPUÉS
<th style={thStyle}>Institución</th>
<th style={thStyle}>Índice S(i) (%)</th>
<th style={thStyle}>Ranking R(i) (0-10)</th>
<th style={thStyle}>Nueva Columna</th>  ← AGREGAR
```

### Paso 2: Agregar dato en la fila

**Línea:** ~117

```javascript
// ANTES
<tr key={item.institucion}>
  <td style={tdStyle}>{item.institucion}</td>
  <td style={tdStyle}>{item.s}</td>
  <td style={tdStyle}>{item.r}</td>
</tr>

// DESPUÉS
<tr key={item.institucion}>
  <td style={tdStyle}>{item.institucion}</td>
  <td style={tdStyle}>{item.s}</td>
  <td style={tdStyle}>{item.r}</td>
  <td style={tdStyle}>{item.nuevoValor}</td>  ← AGREGAR
</tr>
```

---

## 📍 TAREA: Cambiar colores del Heatmap

**Archivo:** `src/App.jsx`  
**Línea:** ~175-180

```javascript
// ANTES (Rojo = Dependiente, Verde = No Usa)
colorScale: {
  ranges: [
    { from: 0, to: 0, color: '#00A100', name: 'No Dependiente' },  // Verde
    { from: 1, to: 1, color: '#FF0000', name: 'Dependiente' },     // Rojo
  ],
},

// DESPUÉS (Personaliza los colores)
colorScale: {
  ranges: [
    { from: 0, to: 0, color: '#CCCCCC', name: 'No Dependiente' },  // Gris
    { from: 1, to: 1, color: '#FF6B6B', name: 'Dependiente' },     // Rojo oscuro
  ],
},
```

---

## 📍 TAREA: Cambiar colores del Radar

**Archivo:** `src/App.jsx`  
**Línea:** ~77-83

```javascript
// ANTES (Rosa = Color principal)
backgroundColor: 'rgba(255, 99, 132, 0.2)',  // Rosa claro
borderColor: 'rgba(255, 99, 132, 1)',        // Rosa intenso

// DESPUÉS (Azul)
backgroundColor: 'rgba(54, 162, 235, 0.2)',   // Azul claro
borderColor: 'rgba(54, 162, 235, 1)',         // Azul intenso

// OTRAS OPCIONES DE COLOR:
// Verde: rgba(75, 192, 75, 0.2) / rgba(75, 192, 75, 1)
// Amarillo: rgba(255, 206, 86, 0.2) / rgba(255, 206, 86, 1)
// Púrpura: rgba(153, 102, 255, 0.2) / rgba(153, 102, 255, 1)
```

---

## 📍 TAREA: Agregar un nuevo componente

**Archivo:** `src/App.jsx`

### Paso 1: Crear el componente (ejemplo)

**Después de HeatmapMatriz() (Línea ~190):**

```javascript
function MiNuevoComponente() {
  const [datos, setDatos] = useState([]);
  
  useEffect(() => {
    axios.get(`${API_BASE_URL}/nuevo-endpoint`)
      .then(response => {
        setDatos(response.data);
      })
      .catch(error => console.error('Error:', error));
  }, []);
  
  return (
    <div>
      {/* Tu contenido aquí */}
    </div>
  );
}
```

### Paso 2: Renderizarlo en App()

**Línea:** ~200 (dentro de `<main>`)

```javascript
<MiNuevoComponente />
```

---

## 📋 TABLA DE REFERENCIAS RÁPIDAS

| Tarea | Archivo | Línea | Acción |
|-------|---------|-------|--------|
| Cambiar URL backend | App.jsx | 18 | Editar `API_BASE_URL` |
| Cambiar endpoint tabla | App.jsx | 100 | Editar `.get()` |
| Cambiar endpoint radar | App.jsx | 70 | Editar `.get()` |
| Cambiar endpoint heatmap | App.jsx | 145 | Editar `.get()` |
| Adaptar extractor tabla | App.jsx | 103 | Editar `.then()` |
| Adaptar extractor radar | App.jsx | 73 | Editar `.then()` |
| Cambiar nombres columnas | App.jsx | 117-120 | Editar `.map()` |
| Mejorar estilos | App.css | ALL | Crear clases CSS |
| Mejorar errores | App.jsx | 104, 75, 151 | Editar `.catch()` |
| Cambiar colores heatmap | App.jsx | 175-180 | Editar `ranges` |
| Cambiar colores radar | App.jsx | 77-83 | Editar `backgroundColor` |

---

## 🚀 Flujo Típico de Trabajo

```
1. Te dan los endpoints del backend
   ↓
2. Cambias API_BASE_URL (línea 18)
   ↓
3. Cambias los nombres de endpoints (líneas 70, 100, 145)
   ↓
4. Ejecutas npm run dev y abres F12
   ↓
5. Ves los datos en console.log()
   ↓
6. Si JSON es diferente, adaptas extractores (líneas 73, 103, 150)
   ↓
7. Pruebas en navegador → ¡Funcionando!
   ↓
8. (Opcional) Mejoras CSS y manejo de errores
```

---

**Última actualización:** 15 de noviembre de 2025
