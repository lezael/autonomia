# ⚡ QUICK REFERENCE CARD - FRONT-END

**Imprime esto o abre en otra pestaña mientras trabajas**

---

## 🚀 EJECUTAR EL PROYECTO

```bash
npm run dev
# → http://localhost:5175/
```

---

## 📁 ARCHIVO PRINCIPAL

```
src/App.jsx
├── RadarDependencia()
├── TablaInstituciones()
├── HeatmapMatriz()
└── App()
```

---

## 🔧 LO QUE CAMBIAR EN FASE 2

### 1. URL del Backend (Línea 18)
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
// ↓ CAMBIAR A:
const API_BASE_URL = 'http://TU-URL-AQUI/api';
```

### 2. Endpoints (Líneas 70, 100, 145)
```javascript
// TABLA
axios.get(`${API_BASE_URL}/instituciones`)
// ↓ CAMBIAR A:
axios.get(`${API_BASE_URL}/tu-endpoint`)

// RADAR
axios.get(`${API_BASE_URL}/radar-dependencia`)

// HEATMAP
axios.get(`${API_BASE_URL}/matriz-dependencia`)
```

### 3. Extractores de Datos (Si JSON es diferente)
```javascript
// ANTES
setDatosTabla(response.data);

// DESPUÉS (si viene en un objeto)
setDatosTabla(response.data.instituciones);
```

---

## 📊 ESTRUCTURA JSON ESPERADA

### Tabla
```json
[
  {"institucion": "Univ_A", "s": -25, "r": 3.5}
]
```

### Radar
```json
{
  "labels": ["Google", "AWS"],
  "valoresDeDependencia": [2, 1]
}
```

### Heatmap
```json
{
  "series": [{"name": "Univ_A", "data": [1, 0]}],
  "categorias": ["Google", "AWS"]
}
```

---

## 🐛 DEBUGGING EN CONSOLA (F12)

### Ver datos que llegan
```javascript
console.log('Datos:', response.data);
```

### Testear endpoint
```javascript
axios.get('http://localhost:8000/api/instituciones')
  .then(r => console.log(r.data))
  .catch(e => console.log('Error:', e.message));
```

### Script rápido de debugging
1. Abre F12 → Console
2. Copia `DEBUG_SCRIPT.js`
3. Ejecuta: `debug.testAllEndpoints()`

---

## ⚠️ ERRORES COMUNES

| Error | Causa | Solución |
|-------|-------|----------|
| CORS Error | Backend no permite tu localhost | Avísale al backend |
| 404 | Endpoint URL incorrecta | Verifica la URL exacta |
| Datos vacíos | JSON tiene otra estructura | Ajusta extractores |
| TypeError | Campo no existe | Usa `console.log()` para ver JSON |

---

## 📚 DOCUMENTOS CLAVE

| Necesito... | Abre... |
|------------|---------|
| Entender el plan | `GUIA_FRONT_END.md` |
| Mi checklist | `CHECKLIST.md` |
| Preguntas para backend | `PREGUNTAS_BACKEND.md` |
| Dónde editar qué | `MAPA_RAPIDO.md` |
| Ejemplos de código | `EJEMPLOS_ADAPTACION.js` |
| Templates | `TEMPLATE_CODIGO.jsx` |
| Debuggear | `DEBUG_SCRIPT.js` |

---

## 📝 COMPONENTES Y SUS LÍNEAS

```
RadarDependencia()        → Líneas 50-88
  useState              → Línea 52-54
  useEffect             → Línea 56-75
  render                → Línea 80-88

TablaInstituciones()      → Líneas 90-128
  useState              → Línea 92-95
  useEffect             → Línea 97-109
  render                → Línea 111-128

HeatmapMatriz()           → Líneas 130-195
  useState              → Línea 132-137
  useEffect             → Línea 139-155
  render                → Línea 157-195

App()                     → Líneas 200-225
```

---

## ✅ CHECKLIST MÍNIMO PARA FASE 2

```
☐ Obtener URLs del backend
☐ Cambiar API_BASE_URL (línea 18)
☐ Cambiar endpoints (líneas 70, 100, 145)
☐ Adaptar extractores si JSON es diferente
☐ Abrir F12 y verificar errores
☐ Ver que gráficos se actualizan
☐ ¡Celebrar! 🎉
```

---

## 🎨 COLORES DEL DASHBOARD

```javascript
// Radar
backgroundColor: 'rgba(255, 99, 132, 0.2)'   // Rosa claro
borderColor: 'rgba(255, 99, 132, 1)'         // Rosa oscuro

// Heatmap
#00A100 → Verde (No dependiente)
#FF0000 → Rojo (Dependiente)
```

---

## 🔀 CAMBIAR COLORES

### Radar (Línea 77-83)
```javascript
backgroundColor: 'rgba(54, 162, 235, 0.2)',  // Azul
borderColor: 'rgba(54, 162, 235, 1)',        // Azul oscuro
```

### Heatmap (Línea 175-180)
```javascript
{ from: 0, to: 0, color: '#00A100' }  // Verde
{ from: 1, to: 1, color: '#FF0000' }  // Rojo
```

---

## 📞 CONTACTO BACKEND

Pregúntales:

1. ¿URL base del API?
2. ¿Los 3 endpoints exactos?
3. ¿Formato JSON de cada uno?
4. ¿Necesito CORS?

**Contactos:**
- Matías Olivares
- Matías Zepeda
- Bastián Tapia

---

## 🆘 SI ALGO FALLA

### Paso 1: Abre F12 → Console
```
¿Ves error? → Lee el error
¿No ves error? → Mira la pestaña Network
```

### Paso 2: Ejecuta DEBUG_SCRIPT.js
```javascript
// En F12 Console, copia y ejecuta:
debug.testAllEndpoints();
```

### Paso 3: Revisa tu JSON
```javascript
// En .then((response) => {
console.log('Datos:', response.data);
// Mira qué estructura tiene
```

---

## 📊 ESTADO DEL PROYECTO

```
FASE 1: ✅ Completada (100%)
  ✅ Interfaz visual
  ✅ 3 componentes
  ✅ Documentación

FASE 2: ⏳ Pendiente (0%)
  ☐ Conectar al backend
  ☐ Datos reales

FASE 3: ⏳ Pendiente (0%)
  ☐ Pulir CSS
  ☐ Mejorar errores
```

---

## 🚀 PRÓXIMOS PASOS (En Orden)

```
1️⃣  Lee GUIA_FRONT_END.md
2️⃣  Lee CHECKLIST.md
3️⃣  Prepara PREGUNTAS_BACKEND.md
4️⃣  Habla con backend
5️⃣  Actualiza src/App.jsx
6️⃣  Prueba en navegador
7️⃣  ¡Celebra! 🎉
```

---

## 💡 TRUCOS ÚTILES

### Ver todos los datos
```javascript
.then((response) => {
  console.table(response.data);  // Tabla más legible
```

### Agregar logging a cada paso
```javascript
console.log('1. Llamando API...');
axios.get(url)
  .then(r => { console.log('2. Datos recibidos:', r.data); setData(r.data); })
  .catch(e => { console.log('3. Error:', e.message); });
```

### Verificar estructura JSON
```javascript
// En DevTools:
JSON.stringify(response.data, null, 2)  // Formato bonito
```

---

## 📏 MEDIDAS DEL DASHBOARD

```
Radar: 600px ancho × auto alto
Tabla: 80% ancho
Heatmap: 80% ancho × 200px alto
Espacios: 40px arriba/abajo
```

---

## 🎯 OBJETIVO FINAL

**Cuando termines Fase 2:**
- ✅ Dashboard muestra datos REALES del backend
- ✅ Los 3 gráficos se actualizan automáticamente
- ✅ No hay errores en F12 Console
- ✅ Todo es interactivo y funcional

---

**Imprime esta tarjeta o tenla a mano mientras trabajas** 📌

---

*Quick Reference Card - Autonometría Digital Frontend*  
*Actualizada: 15 de noviembre de 2025*
