// TEMPLATE: Copia y pega aquí cuando adaptes el código a tu API

// ============================================================================
// TEMPLATE 1: Componente genérico con useState + useEffect + axios
// ============================================================================

function MiComponente() {
  // 1. Define el estado inicial (vacío o con datos de ejemplo)
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  // 2. Llama a la API cuando el componente carga
  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/tu-endpoint`)
      .then((response) => {
        console.log('Datos recibidos:', response.data); // ← Para debuggear
        setDatos(response.data); // O extrae así: response.data.campo
        setCargando(false);
      })
      .catch((error) => {
        console.error('Error en tu-endpoint:', error);
        setError('No se pudieron cargar los datos');
        setCargando(false);
      });
  }, []); // El [] vacío significa que se ejecuta solo una vez

  // 3. Muestra un estado mientras carga
  if (cargando) {
    return <div style={{ textAlign: 'center' }}>Cargando...</div>;
  }

  // 4. Muestra un error si ocurre
  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  // 5. Renderiza con los datos
  return (
    <div>
      {/* Aquí va tu contenido usando "datos" */}
    </div>
  );
}

// ============================================================================
// TEMPLATE 2: Tabla dinámica con datos del backend
// ============================================================================

function Tabla() {
  const [datos, setDatos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/datos-tabla`)
      .then((response) => {
        // AJUSTA ESTO según lo que devuelva tu backend:
        // Option A: Si devuelve un array directo
        setDatos(response.data);
        
        // Option B: Si devuelve un objeto con un campo "datos"
        // setDatos(response.data.datos);
        
        // Option C: Si devuelve un objeto con un campo "items"
        // setDatos(response.data.items);
        
        setCargando(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setError('Error al cargar la tabla');
        setCargando(false);
      });
  }, []);

  if (cargando) return <div>Cargando tabla...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (datos.length === 0) return <div>No hay datos disponibles</div>;

  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ backgroundColor: '#f0f0f0' }}>
          {/* Ajusta estas columnas según tus datos */}
          <th style={{ border: '1px solid #ddd', padding: '12px' }}>Nombre</th>
          <th style={{ border: '1px solid #ddd', padding: '12px' }}>Valor</th>
          <th style={{ border: '1px solid #ddd', padding: '12px' }}>Ranking</th>
        </tr>
      </thead>
      <tbody>
        {datos.map((item, index) => (
          <tr key={index}>
            {/* Ajusta estos campos según lo que devuelva tu API */}
            <td style={{ border: '1px solid #ddd', padding: '12px' }}>
              {item.nombre} {/* O item.institucion, item.nombre, etc */}
            </td>
            <td style={{ border: '1px solid #ddd', padding: '12px' }}>
              {item.valor} {/* O item.s, item.indice, etc */}
            </td>
            <td style={{ border: '1px solid #ddd', padding: '12px' }}>
              {item.ranking} {/* O item.r, item.posicion, etc */}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// ============================================================================
// TEMPLATE 3: Gráfico de Radar con datos dinámicos
// ============================================================================

function RadarDinamico() {
  const [datosRadar, setDatosRadar] = useState({
    labels: [],
    valores: [],
  });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/radar-datos`)
      .then((response) => {
        console.log('Datos radar:', response.data);
        
        // AJUSTA ESTO según lo que devuelva tu backend:
        setDatosRadar({
          labels: response.data.labels, // o response.data.servicios
          valores: response.data.valores, // o response.data.dependencias
        });
        
        setCargando(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setError('Error al cargar el radar');
        setCargando(false);
      });
  }, []);

  if (cargando) return <div>Cargando radar...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  const data = {
    labels: datosRadar.labels,
    datasets: [
      {
        label: 'Dependencia',
        data: datosRadar.valores,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  return <Radar data={data} />;
}

// ============================================================================
// TEMPLATE 4: Heatmap con datos dinámicos
// ============================================================================

function HeatmapDinamico() {
  const [datosHeatmap, setDatosHeatmap] = useState({
    series: [],
    categorias: [],
  });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/heatmap-datos`)
      .then((response) => {
        console.log('Datos heatmap:', response.data);
        
        // AJUSTA ESTO según lo que devuelva tu backend:
        // Si devuelve series e instituciones por separado:
        setDatosHeatmap({
          series: response.data.series,
          categorias: response.data.categorias,
        });
        
        // O si necesitas construir series a partir de la matriz:
        // const series = response.data.instituciones.map((inst, idx) => ({
        //   name: inst,
        //   data: response.data.matriz[idx],
        // }));
        // setDatosHeatmap({
        //   series: series,
        //   categorias: response.data.servicios,
        // });
        
        setCargando(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setError('Error al cargar el heatmap');
        setCargando(false);
      });
  }, []);

  if (cargando) return <div>Cargando heatmap...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  const options = {
    chart: { id: 'heatmap' },
    xaxis: {
      categories: datosHeatmap.categorias,
    },
    plotOptions: {
      heatmap: {
        colorScale: {
          ranges: [
            { from: 0, to: 0, color: '#00A100' },
            { from: 1, to: 1, color: '#FF0000' },
          ],
        },
      },
    },
    dataLabels: {
      enabled: false,
    },
  };

  return <Chart options={options} series={datosHeatmap.series} type="heatmap" />;
}

// ============================================================================
// CONSEJOS DE DEBUGGING
// ============================================================================

/*
1. SIEMPRE usa console.log() después de recibir datos:
   .then((response) => {
     console.log('Datos:', response.data); // ← MIRA ESTO EN F12
     setDatos(response.data);
   })

2. Abre F12 (Developer Tools) y ve a la pestaña:
   - Console → ver errores
   - Network → ver las peticiones HTTP

3. Si ves un error de CORS:
   → Significa que el backend no permite requests desde tu localhost
   → Avísale al equipo de backend

4. Si los datos no aparecen:
   → Compara la estructura JSON que ves en console.log() con lo que espera el código
   → Ajusta los nombres de los campos

5. Si recibiste un 404:
   → La URL del endpoint es incorrecta
   → Verifica en la pestaña Network → XHR → la URL exacta
*/
