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

const API_BASE_URL = '/api';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function RadarDependencia() {
  const [datosRadar, setDatosRadar] = useState({
    labels: ['Google', 'AWS', 'Microsoft', 'Meta'],
    valoresDeDependencia: [2, 1, 2, 1],
  });
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

  const data = {
    labels: datosRadar.labels,
    datasets: [
      {
        label: '# de Instituciones Dependientes',
        data: datosRadar.valoresDeDependencia,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="section-card">
      <h2>📊 Dependencia Total por Servicio</h2>
      {cargandoRadar && (
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando gráfico de radar...</p>
        </div>
      )}
      {errorRadar && (
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos del Radar</strong></div>
          <div className="detalles">{errorRadar}</div>
          <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>Usando datos de ejemplo</p>
        </div>
      )}
      {!cargandoRadar && !errorRadar && (
        <div className="estado-exito">✅ Datos cargados correctamente</div>
      )}
      <div className="grafico-container" style={{ maxWidth: '700px', margin: '0 auto' }}>
        <Radar data={data} />
      </div>
    </div>
  );
}

function TablaInstituciones() {
  const [datosTabla, setDatosTabla] = useState([
    { institucion: 'Univ_A', s: -25, r: 3.5 },
    { institucion: 'Univ_B', s: 67, r: 8.2 },
    { institucion: 'Univ_C', s: -100, r: 0.0 },
  ]);
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

  return (
    <div className="section-card">
      <h2>🏆 Ranking de Soberanía Digital</h2>
      {cargandoTabla && (
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando ranking de instituciones...</p>
        </div>
      )}
      {errorTabla && (
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos de la Tabla</strong></div>
          <div className="detalles">{errorTabla}</div>
          <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>Usando datos de ejemplo</p>
        </div>
      )}
      {!cargandoTabla && !errorTabla && (
        <div className="estado-exito">✅ Datos cargados correctamente</div>
      )}
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
            {datosTabla.map((item) => (
              <tr key={item.institucion}>
                <td className="nombre-institucion">{item.institucion}</td>
                <td className={item.s >= 0 ? 'indice-positivo' : 'indice-negativo'}>
                  {item.s >= 0 ? '+' : ''}{item.s}%
                </td>
                <td>
                  <span className={getRankingClass(item.r)}>{item.r.toFixed(1)}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function HeatmapMatriz() {
  const [datosHeatmap, setDatosHeatmap] = useState({
    series: [
      { name: 'Univ_A', data: [1, 0, 1, 0] },
      { name: 'Univ_B', data: [1, 1, 0, 0] },
      { name: 'Univ_C', data: [0, 0, 1, 1] },
    ],
    categorias: ['Google', 'AWS', 'Microsoft', 'Meta'],
  });
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

  const options = {
    chart: { id: 'heatmap-dependencia' },
    xaxis: {
      categories: datosHeatmap.categorias,
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
      {cargandoHeatmap && (
        <div className="estado-cargando">
          <div className="icono">⏳</div>
          <p>Cargando mapa de calor...</p>
        </div>
      )}
      {errorHeatmap && (
        <div className="estado-error">
          <div className="icono">⚠️</div>
          <div><strong>No se pudieron cargar los datos del Heatmap</strong></div>
          <div className="detalles">{errorHeatmap}</div>
          <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>Usando datos de ejemplo</p>
        </div>
      )}
      {!cargandoHeatmap && !errorHeatmap && (
        <div className="estado-exito">✅ Datos cargados correctamente</div>
      )}
      <div className="grafico-container">
        <Chart
          options={options}
          series={datosHeatmap.series}
          type="heatmap"
          height={300}
        />
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Dashboard de Autonometría Digital</h1>
        <p>Análisis de Soberanía Tecnológica en Instituciones de Educación Superior</p>
        <div className="backend-status">
          <span className="status-dot"></span>
          <span>Conectado a: {API_BASE_URL}</span>
        </div>
      </header>
      <main>
        <RadarDependencia />
        <hr className="separador" />
        <TablaInstituciones />
        <hr className="separador" />
        <HeatmapMatriz />
      </main>
      <footer>
        <p><strong>Dashboard de Autonometría Digital</strong></p>
        <p>Proyecto de análisis de dependencia tecnológica | Frontend en React + Backend en FastAPI</p>
        <p style={{ marginTop: '1rem', fontSize: '0.8rem', opacity: 0.7 }}>Presiona F12 para ver detalles técnicos en consola</p>
      </footer>
    </div>
  );
}

export default App;
