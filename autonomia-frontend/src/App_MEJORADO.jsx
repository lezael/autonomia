// src/App.jsx
// --- TODO EL FRONT-END EN UN SOLO ARCHIVO ---
// --- CONECTADO A LA API DE FASTAPI ---
// --- VERSIÓN MEJORADA CON MEJOR UX PARA CARGA/ERRORES ---

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// --- Importaciones para Gráficos ---
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
import Chart from 'react-apexcharts'; // Para el Heatmap

// --- Configuración de la URL base del Backend ---
// Usamos ruta relativa para que Vite haga proxy a http://localhost:8000
// Esto evita problemas de CORS durante el desarrollo.
const API_BASE_URL = '/api';

// --- Registro de Chart.js (para el Radar) ---
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

// ===================================================================
// COMPONENTES DE ESTADO: Cargando, Error, Éxito
// ===================================================================
function EstadoCargando({ mensaje = 'Cargando...' }) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '20px',
      color: '#666',
      fontSize: '14px',
      backgroundColor: '#f5f5f5',
      borderRadius: '4px',
      margin: '10px 0',
    }}>
      <div style={{ fontSize: '24px', marginBottom: '10px' }}>⏳</div>
      {mensaje}
    </div>
  );
}

function EstadoError({ error, mensaje = 'Error al cargar los datos' }) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '20px',
      color: '#ff9800',
      fontSize: '14px',
      backgroundColor: '#fff3e0',
      borderRadius: '4px',
      margin: '10px 0',
      border: '1px solid #ff9800',
    }}>
      <div style={{ fontSize: '24px', marginBottom: '10px' }}>⚠️</div>
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>{mensaje}</div>
      <div style={{ fontSize: '12px', color: '#999' }}>
        {error}
      </div>
      <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
        ℹ️ Mostrando datos de ejemplo. Verifica que:
        <br />✓ El backend está corriendo en {API_BASE_URL}
        <br />✓ CORS está habilitado (ver CORS_PARA_BACKEND.md)
        <br />✓ Los endpoints existen
      </div>
    </div>
  );
}

function EstadoExito() {
  return (
    <div style={{
      fontSize: '12px',
      color: '#4caf50',
      marginBottom: '10px',
    }}>
      ✅ Datos cargados correctamente
    </div>
  );
}

// ===================================================================
// 1. COMPONENTE: GRÁFICO DE RADAR (CONECTADO A LA API)
// ===================================================================
function RadarDependencia() {
  const [datosRadar, setDatosRadar] = useState({
    labels: ['Google', 'AWS', 'Microsoft', 'Meta'],
    valoresDeDependencia: [2, 1, 2, 1], // Valores por defecto
  });
  const [cargandoRadar, setCargandoRadar] = useState(true);
  const [errorRadar, setErrorRadar] = useState(null);

  useEffect(() => {
    // Llamar a la API para obtener datos del Radar
    console.log('📡 Radar: Intentando conectar a', `${API_BASE_URL}/radar-dependencia`);
    
    axios
      .get(`${API_BASE_URL}/radar-dependencia`)
      .then((response) => {
        console.log('✅ Radar: Datos recibidos correctamente', response.data);
        setDatosRadar(response.data);
        setErrorRadar(null);
        setCargandoRadar(false);
      })
      .catch((error) => {
        console.error('❌ Radar: Error al traer datos', {
          mensaje: error.message,
          codigo: error.code,
          response: error.response?.status,
        });
        setErrorRadar(error.message);
        setCargandoRadar(false);
        // Mantener los datos de ejemplo si hay error
      });
  }, []);

  return (
    <div style={{ width: '600px', margin: 'auto' }}>
      <h2>Dependencia Total por Servicio</h2>
      {cargandoRadar && <EstadoCargando mensaje="⏳ Cargando gráfico de Radar..." />}
      {errorRadar && <EstadoError error={errorRadar} />}
      {!cargandoRadar && !errorRadar && <EstadoExito />}
      
      <Radar data={{
        labels: datosRadar.labels,
        datasets: [{
          label: '# de Instituciones Dependientes',
          data: datosRadar.valoresDeDependencia,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        }],
      }} />
    </div>
  );
}

// ===================================================================
// 2. COMPONENTE: TABLA DE INSTITUCIONES (CONECTADO A LA API)
// ===================================================================
function TablaInstituciones() {
  const [datosTabla, setDatosTabla] = useState([
    { institucion: 'Univ_A', s: -25, r: 3.5 },
    { institucion: 'Univ_B', s: 67, r: 8.2 },
    { institucion: 'Univ_C', s: -100, r: 0.0 },
  ]);
  const [cargandoTabla, setCargandoTabla] = useState(true);
  const [errorTabla, setErrorTabla] = useState(null);

  useEffect(() => {
    // Llamar a la API para obtener datos de instituciones
    console.log('📡 Tabla: Intentando conectar a', `${API_BASE_URL}/instituciones`);
    
    axios
      .get(`${API_BASE_URL}/instituciones`)
      .then((response) => {
        console.log('✅ Tabla: Datos recibidos correctamente', response.data);
        setDatosTabla(response.data);
        setErrorTabla(null);
        setCargandoTabla(false);
      })
      .catch((error) => {
        console.error('❌ Tabla: Error al traer datos', {
          mensaje: error.message,
          codigo: error.code,
          response: error.response?.status,
        });
        setErrorTabla(error.message);
        setCargandoTabla(false);
        // Mantener los datos de ejemplo si hay error
      });
  }, []);

  const thStyle = { border: '1px solid #ddd', padding: '12px', textAlign: 'left' };
  const tdStyle = { border: '1px solid #ddd', padding: '12px' };

  return (
    <div style={{ width: '80%', margin: '40px auto' }}>
      <h2>Ranking de Soberanía Digital</h2>
      {cargandoTabla && <EstadoCargando mensaje="⏳ Cargando tabla..." />}
      {errorTabla && <EstadoError error={errorTabla} />}
      {!cargandoTabla && !errorTabla && <EstadoExito />}
      
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ backgroundColor: '#f0f0f0' }}>
            <th style={thStyle}>Institución</th>
            <th style={thStyle}>Índice S(i) (%)</th>
            <th style={thStyle}>Ranking R(i) (0-10)</th>
          </tr>
        </thead>
        <tbody>
          {datosTabla.map((item) => (
            <tr key={item.institucion}>
              <td style={tdStyle}>{item.institucion}</td>
              <td style={tdStyle}>{item.s}</td>
              <td style={tdStyle}>{item.r}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ===================================================================
// 3. COMPONENTE: HEATMAP MATRICIAL (CONECTADO A LA API)
// ===================================================================
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
    // Llamar a la API para obtener datos de la matriz de dependencia
    console.log('📡 Heatmap: Intentando conectar a', `${API_BASE_URL}/matriz-dependencia`);
    
    axios
      .get(`${API_BASE_URL}/matriz-dependencia`)
      .then((response) => {
        console.log('✅ Heatmap: Datos recibidos correctamente', response.data);
        setDatosHeatmap(response.data);
        setErrorHeatmap(null);
        setCargandoHeatmap(false);
      })
      .catch((error) => {
        console.error('❌ Heatmap: Error al traer datos', {
          mensaje: error.message,
          codigo: error.code,
          response: error.response?.status,
        });
        setErrorHeatmap(error.message);
        setCargandoHeatmap(false);
        // Mantener los datos de ejemplo si hay error
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
    <div style={{ width: '80%', margin: '40px auto' }}>
      <h2>Heatmap Matricial de Dependencia</h2>
      {cargandoHeatmap && <EstadoCargando mensaje="⏳ Cargando heatmap..." />}
      {errorHeatmap && <EstadoError error={errorHeatmap} />}
      {!cargandoHeatmap && !errorHeatmap && <EstadoExito />}
      
      <Chart
        options={options}
        series={datosHeatmap.series}
        type="heatmap"
        height={200}
      />
    </div>
  );
}

// ===================================================================
// APLICACIÓN PRINCIPAL (Dashboard)
// ===================================================================
function App() {
  return (
    <div className="App">
      <header className="App-header" style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
        <h1>Dashboard de Autonometría Digital</h1>
        <p style={{ fontSize: '14px', color: '#666', margin: '10px 0 0 0' }}>
          🔌 Backend: {API_BASE_URL}
        </p>
        <p style={{ fontSize: '12px', color: '#999', margin: '5px 0' }}>
          Si ves ⚠️ de error, revisa la consola (F12) y el archivo CORS_PARA_BACKEND.md
        </p>
      </header>
      <main>
        {/* Renderiza todos los componentes */}

        <RadarDependencia />

        <hr style={{ width: '80%', margin: '40px auto' }} />

        <TablaInstituciones />

        <hr style={{ width: '80%', margin: '40px auto' }} />

        <HeatmapMatriz />

      </main>
      
      {/* Footer con información de debug */}
      <footer style={{ textAlign: 'center', padding: '20px', backgroundColor: '#f5f5f5', borderTop: '1px solid #ddd', marginTop: '40px', fontSize: '12px', color: '#999' }}>
        <p>Dashboard de Autonometría Digital | Fronted en React</p>
        <p>Abre F12 → Console para ver detalles de conexión y errores</p>
      </footer>
    </div>
  );
}

export default App;
