import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import Chart from 'react-apexcharts';

const API_BASE_URL = 'http://localhost:8000/api';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

// ============================================================================
// NUEVO COMPONENTE: FORMULARIO DE ANÁLISIS
// ============================================================================

function FormularioAnalisis({ onAnalisisCompletado }) {
  const [url, setUrl] = useState('');
  const [analizando, setAnalizando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAnalizando(true);
    setError(null);
    setResultado(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analizar`, { url });
      setResultado(response.data);
      if (onAnalisisCompletado) {
        onAnalisisCompletado(response.data);
      }
    } catch (err) {
      console.error('Error al analizar:', err);
      setError(err.response?.data?.detail || 'Error al analizar la URL');
    } finally {
      setAnalizando(false);
    }
  };

  return (
    <div className="section-card">
      <h2>🔍 Analizar Institución</h2>
      <form onSubmit={handleSubmit} className="formulario-analisis">
        <div className="input-group">
          <input
            type="url"
            placeholder="https://www.universidad.edu.ar"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            className="input-url"
            disabled={analizando}
          />
          <button type="submit" disabled={analizando} className="btn-analizar">
            {analizando ? '⏳ Analizando...' : '🚀 Analizar'}
          </button>
        </div>
      </form>

      {error && (
        <div className="estado-error" style={{ marginTop: '1rem' }}>
          <div className="icono">❌</div>
          <div><strong>Error en el análisis</strong></div>
          <div className="detalles">{error}</div>
        </div>
      )}

      {resultado && (
        <div className="resultado-analisis">
          <div className="estado-exito">
            ✅ Análisis completado: {resultado.tecnologias_detectadas?.length || 0} tecnologías detectadas
          </div>

          {/* Métricas Principales */}
          <div className="metricas-grid">
            <div className="metrica-card">
              <h3>📊 Índice de Soberanía S(i)</h3>
              <div className="valor-grande">
                {(resultado.indice_soberania * 100).toFixed(1)}%
              </div>
              <div className="descripcion">
                {resultado.tecnologias_libres_count || 0} libres / {resultado.tecnologias_privativas_count || 0} privativas
              </div>
            </div>

            <div className="metrica-card">
              <h3>⭐ Ranking R(i)</h3>
              <div className="valor-grande">
                {(resultado.ranking_normalizado * 10).toFixed(1)}/10
              </div>
              <div className="descripcion">
                Escala normalizada
              </div>
            </div>
          </div>

          {/* Tecnologías Detectadas */}
          {resultado.tecnologias_detectadas && resultado.tecnologias_detectadas.length > 0 && (
            <div className="tecnologias-detectadas">
              <h3>🔍 Tecnologías Detectadas</h3>
              <div className="tecnologias-grid">
                {resultado.tecnologias_detectadas.map((tech, idx) => (
                  <div
                    key={idx}
                    className={`tech-badge ${tech.tipo === 'libre' ? 'tech-libre' : 'tech-privativo'}`}
                  >
                    <span className="tech-nombre">{tech.nombre}</span>
                    <span className="tech-tipo">
                      {tech.tipo === 'libre' ? '✅ Libre' : '⚠️ Privativo'}
                    </span>
                    <span className="tech-categoria">{tech.categoria}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recomendaciones */}
          {resultado.recomendaciones && resultado.recomendaciones.length > 0 && (
            <div className="recomendaciones">
              <h3>💡 Recomendaciones</h3>
              <ul>
                {resultado.recomendaciones.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Matriz de Dependencia */}
          {resultado.matriz_dependencia && (
            <div className="matriz-info">
              <h3>🔢 Matriz de Dependencia</h3>
              <p>Dimensiones: {resultado.matriz_dependencia.length} × {resultado.matriz_dependencia[0]?.length || 0}</p>
              <code>{JSON.stringify(resultado.matriz_dependencia)}</code>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// COMPONENTE: RADAR DE DEPENDENCIA (MEJORADO)
// ============================================================================

function RadarDependencia() {
  const [datosRadar, setDatosRadar] = useState(null);
  const [cargandoRadar, setCargandoRadar] = useState(true);
  const [errorRadar, setErrorRadar] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/radar-dependencia`)
      .then((response) => {
        setDatosRadar(response.data);
        setCargandoRadar(false);
      })
      .catch((error) => {
        console.error('Error al traer datos del Radar:', error);
        setErrorRadar('No se pudieron cargar los datos del Radar');
        setCargandoRadar(false);
      });
  }, []);

  if (cargandoRadar) {
    return (
      <div className="section-card">
        <h2>📊 Dependencia Total por Servicio</h2>
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando gráfico de radar...</p>
        </div>
      </div>
    );
  }

  if (errorRadar || !datosRadar) {
    return (
      <div className="section-card">
        <h2>📊 Dependencia Total por Servicio</h2>
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos del Radar</strong></div>
        </div>
      </div>
    );
  }

  const data = {
    labels: datosRadar.categorias || ['Analítica', 'CDN', 'CMS', 'LMS', 'Hosting'],
    datasets: datosRadar.series?.map((serie, idx) => ({
      label: serie.nombre,
      data: serie.data,
      backgroundColor: `rgba(${idx * 100}, 99, 132, 0.2)`,
      borderColor: `rgba(${idx * 100}, 99, 132, 1)`,
      borderWidth: 2,
    })) || [],
  };

  return (
    <div className="section-card">
      <h2>📊 Dependencia Total por Servicio</h2>
      <div className="estado-exito">✅ Datos cargados correctamente</div>
      <div className="grafico-container" style={{ maxWidth: '700px', margin: '0 auto' }}>
        <Radar data={data} />
      </div>
    </div>
  );
}

// ============================================================================
// COMPONENTE: TABLA DE INSTITUCIONES (ARREGLADO)
// ============================================================================

function TablaInstituciones() {
  const [datosTabla, setDatosTabla] = useState([]);
  const [cargandoTabla, setCargandoTabla] = useState(true);
  const [errorTabla, setErrorTabla] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/instituciones`)
      .then((response) => {
        setDatosTabla(response.data);
        setCargandoTabla(false);
      })
      .catch((error) => {
        console.error('Error al traer datos de la Tabla:', error);
        setErrorTabla('No se pudieron cargar los datos de la Tabla');
        setCargandoTabla(false);
      });
  }, []);

  const getRankingClass = (ranking) => {
    if (ranking >= 7) return 'badge-ranking badge-alto';
    if (ranking >= 5) return 'badge-ranking badge-medio';
    return 'badge-ranking badge-bajo';
  };

  if (cargandoTabla) {
    return (
      <div className="section-card">
        <h2>🏆 Ranking de Soberanía Digital</h2>
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando ranking de instituciones...</p>
        </div>
      </div>
    );
  }

  if (errorTabla || !datosTabla || datosTabla.length === 0) {
    return (
      <div className="section-card">
        <h2>🏆 Ranking de Soberanía Digital</h2>
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos</strong></div>
        </div>
      </div>
    );
  }

  return (
    <div className="section-card">
      <h2>🏆 Ranking de Soberanía Digital</h2>
      <div className="estado-exito">✅ Datos cargados correctamente</div>
      <div className="tabla-container">
        <table className="tabla-instituciones">
          <thead>
            <tr>
              <th>Institución</th>
              <th>Índice S(i) (%)</th>
              <th>Ranking R(i)</th>
            </tr>
          </thead>
          <tbody>
            {datosTabla.map((item, idx) => {
              const soberaniaPercent = ((item.indice_soberania || item.soberania || 0) * 100).toFixed(0);
              const ranking = (item.ranking_normalizado || item.ranking || 0) * 10;
              
              return (
                <tr key={idx}>
                  <td className="nombre-institucion">{item.nombre || item.institucion}</td>
                  <td className={soberaniaPercent >= 50 ? 'indice-positivo' : 'indice-negativo'}>
                    {soberaniaPercent >= 0 ? '+' : ''}{soberaniaPercent}%
                  </td>
                  <td>
                    <span className={getRankingClass(ranking)}>{ranking.toFixed(1)}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ============================================================================
// COMPONENTE: HEATMAP (MEJORADO)
// ============================================================================

function HeatmapMatriz() {
  const [datosHeatmap, setDatosHeatmap] = useState(null);
  const [cargandoHeatmap, setCargandoHeatmap] = useState(true);
  const [errorHeatmap, setErrorHeatmap] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/matriz-dependencia`)
      .then((response) => {
        setDatosHeatmap(response.data);
        setCargandoHeatmap(false);
      })
      .catch((error) => {
        console.error('Error al traer datos del Heatmap:', error);
        setErrorHeatmap('No se pudieron cargar los datos del Heatmap');
        setCargandoHeatmap(false);
      });
  }, []);

  if (cargandoHeatmap) {
    return (
      <div className="section-card">
        <h2>🔥 Heatmap Matricial de Dependencia</h2>
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando mapa de calor...</p>
        </div>
      </div>
    );
  }

  if (errorHeatmap || !datosHeatmap) {
    return (
      <div className="section-card">
        <h2>🔥 Heatmap Matricial de Dependencia</h2>
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos del Heatmap</strong></div>
        </div>
      </div>
    );
  }

  const options = {
    chart: { id: 'heatmap-dependencia' },
    xaxis: {
      categories: datosHeatmap.tecnologias || datosHeatmap.categorias || [],
    },
    plotOptions: {
      heatmap: {
        colorScale: {
          ranges: [
            { from: 0, to: 0, color: '#00A100', name: 'No Dependiente' },
            { from: 1, to: 1, color: '#FF0000', name: 'Dependiente' },
          ],
        },
      },
    },
    dataLabels: {
      enabled: false,
    },
    title: {
      text: 'Heatmap de Matriz de Dependencia (D)',
    },
  };

  return (
    <div className="section-card">
      <h2>🔥 Heatmap Matricial de Dependencia</h2>
      <div className="estado-exito">✅ Datos cargados correctamente</div>
      <div className="grafico-container">
        <Chart
          options={options}
          series={datosHeatmap.series || []}
          type="heatmap"
          height={300}
        />
      </div>
    </div>
  );
}

// ============================================================================
// APP PRINCIPAL
// ============================================================================

function App() {
  const [ultimoAnalisis, setUltimoAnalisis] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 AutonomIA - Dashboard de Soberanía Digital</h1>
        <p>Análisis Matemático de Soberanía Tecnológica en Instituciones</p>
        <div className="backend-status">
          <span className="status-dot"></span>
          <span>Backend: http://localhost:8000</span>
        </div>
      </header>

      <main>
        {/* NUEVO: Formulario de Análisis */}
        <FormularioAnalisis onAnalisisCompletado={setUltimoAnalisis} />

        <hr className="separador" />

        {/* Componentes existentes */}
        <TablaInstituciones />
        
        <hr className="separador" />
        
        <RadarDependencia />
        
        <hr className="separador" />
        
        <HeatmapMatriz />
      </main>

      <footer>
        <p><strong>AutonomIA - Análisis de Soberanía Tecnológica</strong></p>
        <p>Backend: FastAPI + Python | Frontend: React + Chart.js</p>
        <p style={{ marginTop: '1rem', fontSize: '0.8rem', opacity: 0.7 }}>
          Presiona F12 para ver detalles técnicos en consola
        </p>
      </footer>
    </div>
  );
}

export default App;
