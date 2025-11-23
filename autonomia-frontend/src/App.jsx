import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

const API_BASE_URL = 'http://localhost:8000/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
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
// COMPONENTE: GRÁFICO DE BARRAS DE DEPENDENCIA
// ============================================================================

function GraficoDependencia() {
  const [datosGrafico, setDatosGrafico] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cargarDatos = () => {
      axios
        .get(`${API_BASE_URL}/radar-dependencia`)
        .then((response) => {
          console.log('Datos gráfico:', response.data);
          setDatosGrafico(response.data);
          setCargando(false);
        })
        .catch((error) => {
          console.error('Error al traer datos del gráfico:', error);
          setError('No se pudieron cargar los datos');
          setCargando(false);
        });
    };

    cargarDatos();
    const interval = setInterval(cargarDatos, 5000);
    return () => clearInterval(interval);
  }, []);

  if (cargando) {
    return (
      <div className="section-card">
        <h2>📊 Dependencia por Categoría de Servicio</h2>
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando gráfico...</p>
        </div>
      </div>
    );
  }

  if (error || !datosGrafico || !datosGrafico.categorias || datosGrafico.categorias.length === 0) {
    return (
      <div className="section-card">
        <h2>📊 Dependencia por Categoría de Servicio</h2>
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No hay datos disponibles</strong></div>
          <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>Analiza algunas URLs primero</p>
        </div>
      </div>
    );
  }

  const colores = [
    { bg: 'rgba(102, 126, 234, 0.8)', border: 'rgb(102, 126, 234)' },
    { bg: 'rgba(255, 99, 132, 0.8)', border: 'rgb(255, 99, 132)' },
    { bg: 'rgba(75, 192, 192, 0.8)', border: 'rgb(75, 192, 192)' },
    { bg: 'rgba(255, 206, 86, 0.8)', border: 'rgb(255, 206, 86)' },
    { bg: 'rgba(153, 102, 255, 0.8)', border: 'rgb(153, 102, 255)' },
  ];

  const data = {
    labels: datosGrafico.categorias,
    datasets: datosGrafico.series?.map((serie, idx) => {
      const color = colores[idx % colores.length];
      return {
        label: serie.nombre,
        data: serie.data,
        backgroundColor: color.bg,
        borderColor: color.border,
        borderWidth: 2,
        borderRadius: 6,
        barThickness: 'flex',
        maxBarThickness: 60,
      };
    }) || [],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: datosGrafico.series.length > 1,
        position: 'top',
        align: 'center',
        labels: {
          padding: 15,
          font: {
            size: 14,
            weight: '600',
            family: "'Inter', 'system-ui', sans-serif"
          },
          color: '#333',
          usePointStyle: true,
          pointStyle: 'rectRounded',
          boxWidth: 12,
          boxHeight: 12,
          generateLabels: function(chart) {
            const datasets = chart.data.datasets;
            return datasets.map((dataset, i) => ({
              text: dataset.label,
              fillStyle: dataset.backgroundColor,
              strokeStyle: dataset.borderColor,
              lineWidth: dataset.borderWidth,
              hidden: !chart.isDatasetVisible(i),
              index: i
            }));
          }
        }
      },
      title: {
        display: true,
        text: 'Tecnologías Privativas Detectadas',
        font: {
          size: 18,
          weight: 'bold',
          family: "'Inter', 'system-ui', sans-serif"
        },
        color: '#1a1a1a',
        padding: {
          top: 10,
          bottom: 25
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        padding: 16,
        titleFont: {
          size: 15,
          weight: 'bold'
        },
        bodyFont: {
          size: 14
        },
        bodySpacing: 8,
        displayColors: true,
        boxWidth: 12,
        boxHeight: 12,
        boxPadding: 6,
        callbacks: {
          title: function(context) {
            return context[0].label;
          },
          label: function(context) {
            const sitio = context.dataset.label;
            const valor = context.parsed.y;
            return ` ${sitio}: ${valor} ${valor === 1 ? 'tecnología' : 'tecnologías'}`;
          },
          afterLabel: function(context) {
            return context.parsed.y > 0 ? '⚠️ Privativas' : '✅ Sin dependencias';
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false,
          drawBorder: false
        },
        ticks: {
          color: '#1a1a1a',
          font: {
            size: 13,
            weight: '700',
            family: "'Inter', 'system-ui', sans-serif"
          },
          padding: 12,
          autoSkip: false,
          maxRotation: 0,
          minRotation: 0
        },
        title: {
          display: true,
          text: '📂 Categorías de Tecnología',
          color: '#4a4a4a',
          font: {
            size: 14,
            weight: '700',
            family: "'Inter', 'system-ui', sans-serif"
          },
          padding: {
            top: 20,
            bottom: 0
          }
        }
      },
      y: {
        beginAtZero: true,
        grace: '5%',
        grid: {
          color: 'rgba(0, 0, 0, 0.06)',
          drawBorder: false,
          lineWidth: 1
        },
        ticks: {
          color: '#4a4a4a',
          font: {
            size: 13,
            weight: '600'
          },
          padding: 12,
          stepSize: 1,
          precision: 0,
          callback: function(value) {
            if (Number.isInteger(value)) {
              return value;
            }
          }
        },
        title: {
          display: true,
          text: '📊 Cantidad de Tecnologías Privativas',
          color: '#4a4a4a',
          font: {
            size: 14,
            weight: '700',
            family: "'Inter', 'system-ui', sans-serif"
          },
          padding: {
            bottom: 20,
            top: 0
          }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    },
    layout: {
      padding: {
        top: 10,
        right: 20,
        bottom: 10,
        left: 20
      }
    }
  };

  return (
    <div className="section-card">
      <h2>📊 Análisis de Dependencias por Categoría</h2>
      <div className="estado-exito">
        ✅ {datosGrafico.series?.length || 0} {datosGrafico.series?.length === 1 ? 'sitio analizado' : 'sitios analizados'}
      </div>
      <p style={{ 
        color: '#666', 
        fontSize: '0.95rem', 
        marginTop: '0.8rem', 
        marginBottom: '1.8rem',
        lineHeight: '1.5'
      }}>
        <strong>¿Qué muestra este gráfico?</strong> Compara cuántas tecnologías privativas usa cada sitio en diferentes categorías (Analítica, CDN, etc.). 
        Barras más altas = mayor dependencia de software privativo.
      </p>
      <div style={{ 
        width: '100%', 
        height: '480px',
        padding: '2rem',
        backgroundColor: '#fafbfc',
        borderRadius: '12px',
        boxShadow: '0 2px 12px rgba(0,0,0,0.06)',
        border: '1px solid rgba(0,0,0,0.06)'
      }}>
        <Bar data={data} options={options} />
      </div>
      
      {/* Nota explicativa */}
      <div style={{
        marginTop: '1.5rem',
        padding: '1rem 1.5rem',
        backgroundColor: '#f0f4ff',
        borderLeft: '4px solid #667eea',
        borderRadius: '6px'
      }}>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#444' }}>
          💡 <strong>Interpretación:</strong> Cada barra representa un tipo de tecnología (Analítica, CDN, CMS, etc.). 
          {datosGrafico.series?.length > 1 
            ? ' Los colores distinguen entre diferentes sitios web analizados.' 
            : ' Analiza más URLs para comparar sitios.'}
        </p>
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

  return (
    <div className="section-card">
      <h2>🔥 Matriz de Dependencia</h2>
      <div className="estado-exito">✅ Datos cargados correctamente</div>
      <div className="matriz-visualizacion">
        <table className="matriz-tabla">
          <thead>
            <tr>
              <th>Institución/Tecnología</th>
              {(datosHeatmap.tecnologias || datosHeatmap.categorias || []).map((tech, idx) => (
                <th key={idx}>{tech}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {(datosHeatmap.series || []).map((serie, idx) => (
              <tr key={idx}>
                <td><strong>{serie.name || serie.nombre}</strong></td>
                {(serie.data || []).map((valor, cellIdx) => (
                  <td 
                    key={cellIdx} 
                    className={valor === 1 ? 'cell-dependiente' : 'cell-libre'}
                    style={{
                      backgroundColor: valor === 1 ? '#ff6b6b' : '#51cf66',
                      color: 'white',
                      textAlign: 'center',
                      fontWeight: 'bold'
                    }}
                  >
                    {valor}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
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
        
        <GraficoDependencia />
        
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
