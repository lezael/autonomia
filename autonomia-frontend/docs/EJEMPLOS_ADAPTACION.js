// EJEMPLOS DE ADAPTACIÓN - Copia aquí cuando tengas los datos del backend

// ============================================================================
// EJEMPLO 1: Si tu backend devuelve un formato JSON diferente
// ============================================================================

// SUPONGAMOS que el backend devuelve:
// GET http://localhost:8000/api/instituciones
// Respuesta:
/*
{
  "success": true,
  "data": {
    "rankings": [
      {"id": 1, "nombre": "Universidad A", "indice_soberania": -25, "posicion": 3.5},
      {"id": 2, "nombre": "Universidad B", "indice_soberania": 67, "posicion": 8.2}
    ]
  }
}
*/

// ENTONCES en TablaInstituciones, cambiarías esto:

// VERSIÓN ACTUAL (línea ~95):
// .then((response) => {
//   setDatosTabla(response.data);

// VERSIÓN ADAPTADA:
// .then((response) => {
//   // Extrae el array del JSON anidado
//   setDatosTabla(response.data.data.rankings);
//   // O simplemente:
//   // setDatosTabla(response.data);
// })

// Y luego cambiarías cómo se accede a los datos:
// ACTUAL:
// {datosTabla.map((item) => (
//   <tr key={item.institucion}>
//     <td style={tdStyle}>{item.institucion}</td>
//     <td style={tdStyle}>{item.s}</td>
//     <td style={tdStyle}>{item.r}</td>

// ADAPTADO:
// {datosTabla.map((item) => (
//   <tr key={item.id}>
//     <td style={tdStyle}>{item.nombre}</td>
//     <td style={tdStyle}>{item.indice_soberania}</td>
//     <td style={tdStyle}>{item.posicion}</td>

// ============================================================================
// EJEMPLO 2: Si el Radar necesita datos en un formato diferente
// ============================================================================

// SUPONGAMOS que el backend devuelve:
// GET http://localhost:8000/api/dependencia-servicios
// Respuesta:
/*
{
  "servicios": ["Google", "AWS", "Microsoft", "Meta"],
  "total_dependencias": [2, 1, 2, 1]
}
*/

// ENTONCES en RadarDependencia, cambiarías esto:

// VERSIÓN ACTUAL (línea ~60):
// const [datosRadar, setDatosRadar] = useState({
//   labels: ['Google', 'AWS', 'Microsoft', 'Meta'],
//   valoresDeDependencia: [2, 1, 2, 1],
// });
// ...
// .then((response) => {
//   setDatosRadar(response.data);

// VERSIÓN ADAPTADA:
// .then((response) => {
//   setDatosRadar({
//     labels: response.data.servicios,
//     valoresDeDependencia: response.data.total_dependencias,
//   });

// ============================================================================
// EJEMPLO 3: Si el Heatmap necesita datos en un formato diferente
// ============================================================================

// SUPONGAMOS que el backend devuelve:
// GET http://localhost:8000/api/matriz-dependencia
// Respuesta:
/*
{
  "instituciones": ["Univ_A", "Univ_B", "Univ_C"],
  "servicios": ["Google", "AWS", "Microsoft", "Meta"],
  "matriz": [
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1]
  ]
}
*/

// ENTONCES en HeatmapMatriz, cambiarías esto:

// VERSIÓN ACTUAL (línea ~145):
// const [datosHeatmap, setDatosHeatmap] = useState({
//   series: [
//     { name: 'Univ_A', data: [1, 0, 1, 0] },
//     { name: 'Univ_B', data: [1, 1, 0, 0] },
//     { name: 'Univ_C', data: [0, 0, 1, 1] },
//   ],
//   categorias: ['Google', 'AWS', 'Microsoft', 'Meta'],
// });
// ...
// .then((response) => {
//   setDatosHeatmap(response.data);

// VERSIÓN ADAPTADA:
// .then((response) => {
//   const series = response.data.instituciones.map((inst, idx) => ({
//     name: inst,
//     data: response.data.matriz[idx],
//   }));
//   setDatosHeatmap({
//     series: series,
//     categorias: response.data.servicios,
//   });

// ============================================================================
// CONSEJO FINAL: USA CONSOLE.LOG PARA DEBUGGEAR
// ============================================================================

// Antes de cambiar nada, coloca console.log para ver exactamente
// qué datos devuelve el backend:

// .then((response) => {
//   console.log('Datos del backend:', response.data); // ← Mira esto en F12
//   setDatosTabla(response.data);
// })
