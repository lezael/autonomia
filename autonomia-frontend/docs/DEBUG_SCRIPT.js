// SCRIPT DE DEBUGGING RÁPIDO
// Copia y pega esto en la consola del navegador (F12 → Console)
// para ver si la API está respondiendo correctamente

// ============================================================================
// TEST 1: Verificar que axios está disponible
// ============================================================================
console.log('✓ axios disponible:', typeof axios !== 'undefined');

// ============================================================================
// TEST 2: Verificar la URL base del API
// ============================================================================
const API_BASE_URL = 'http://localhost:8000/api';
console.log('📍 API Base URL:', API_BASE_URL);

// ============================================================================
// TEST 3: Probar la conexión a cada endpoint
// ============================================================================

console.log('\n🔍 Probando conexiones...\n');

// Test Endpoint 1: Instituciones
axios.get(`${API_BASE_URL}/instituciones`)
  .then(response => {
    console.log('✅ ENDPOINT /instituciones FUNCIONA');
    console.log('   Respuesta:', response.data);
  })
  .catch(error => {
    console.log('❌ ENDPOINT /instituciones FALLA');
    console.log('   Error:', error.message);
  });

// Test Endpoint 2: Radar
axios.get(`${API_BASE_URL}/radar-dependencia`)
  .then(response => {
    console.log('✅ ENDPOINT /radar-dependencia FUNCIONA');
    console.log('   Respuesta:', response.data);
  })
  .catch(error => {
    console.log('❌ ENDPOINT /radar-dependencia FALLA');
    console.log('   Error:', error.message);
  });

// Test Endpoint 3: Heatmap
axios.get(`${API_BASE_URL}/matriz-dependencia`)
  .then(response => {
    console.log('✅ ENDPOINT /matriz-dependencia FUNCIONA');
    console.log('   Respuesta:', response.data);
  })
  .catch(error => {
    console.log('❌ ENDPOINT /matriz-dependencia FALLA');
    console.log('   Error:', error.message);
  });

// ============================================================================
// TEST 4: Función útil para probar un endpoint personalizado
// ============================================================================

function testEndpoint(url) {
  console.log(`\n🧪 Probando: ${url}`);
  axios.get(url)
    .then(response => {
      console.log('✅ FUNCIONA');
      console.log('Respuesta:', response.data);
      return response.data;
    })
    .catch(error => {
      console.log('❌ ERROR:', error.message);
      if (error.response) {
        console.log('   Status:', error.response.status);
        console.log('   Data:', error.response.data);
      }
    });
}

// Uso: testEndpoint('http://localhost:8000/api/tu-endpoint')

// ============================================================================
// TEST 5: Verificar si el backend está corriendo
// ============================================================================

axios.head('http://localhost:8000/')
  .then(() => {
    console.log('\n✅ Backend en http://localhost:8000/ ESTÁ ACTIVO');
  })
  .catch(() => {
    console.log('\n❌ Backend en http://localhost:8000/ NO RESPONDE');
    console.log('   Asegúrate de que el servidor FastAPI está corriendo');
  });

// ============================================================================
// TEST 6: Estructura esperada de los datos
// ============================================================================

console.log('\n📋 ESTRUCTURA ESPERADA DE DATOS:\n');

console.log('Para /instituciones:');
console.log(`
{
  institucion: "Univ_A",
  s: -25,
  r: 3.5
}
`);

console.log('Para /radar-dependencia:');
console.log(`
{
  labels: ["Google", "AWS", "Microsoft", "Meta"],
  valoresDeDependencia: [2, 1, 2, 1]
}
`);

console.log('Para /matriz-dependencia:');
console.log(`
{
  series: [
    { name: "Univ_A", data: [1, 0, 1, 0] },
    { name: "Univ_B", data: [1, 1, 0, 0] },
    { name: "Univ_C", data: [0, 0, 1, 1] }
  ],
  categorias: ["Google", "AWS", "Microsoft", "Meta"]
}
`);

// ============================================================================
// TEST 7: Copiar esta función para debuggear rápidamente
// ============================================================================

window.debug = {
  testAllEndpoints: function() {
    console.log('Probando todos los endpoints...');
    testEndpoint(`${API_BASE_URL}/instituciones`);
    testEndpoint(`${API_BASE_URL}/radar-dependencia`);
    testEndpoint(`${API_BASE_URL}/matriz-dependencia`);
  },
  
  testCustom: function(endpoint) {
    testEndpoint(`${API_BASE_URL}${endpoint}`);
  },
  
  checkBackend: function(url) {
    console.log(`Verificando si ${url} está disponible...`);
    axios.head(url)
      .then(() => console.log('✅ Disponible'))
      .catch(() => console.log('❌ No disponible'));
  }
};

console.log('\n💡 FUNCIONES DE DEBUGGING DISPONIBLES:');
console.log('debug.testAllEndpoints()    → Prueba los 3 endpoints principales');
console.log('debug.testCustom("/url")    → Prueba un endpoint personalizado');
console.log('debug.checkBackend("url")   → Verifica si un servidor está disponible');
console.log('testEndpoint("url")         → Función genérica de prueba');
