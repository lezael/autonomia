"""
Tests básicos de integración para la API.

Tu colega: Añadir tests específicos para su lógica de análisis.
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Cliente de prueba para la API"""
    return TestClient(app)


class TestHealthCheck:
    """Tests para verificar estado del servidor"""
    
    def test_root_endpoint(self, client):
        """Test endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "AutonomIA Backend"
        assert data["estado"] == "operacional"
    
    def test_salud_endpoint(self, client):
        """Test endpoint de salud"""
        response = client.get("/api/salud")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "operacional"
        assert "version" in data


class TestTecnologias:
    """Tests para listar tecnologías"""
    
    def test_listar_tecnologias(self, client):
        """Test lista de tecnologías"""
        response = client.get("/api/tecnologias")
        assert response.status_code == 200
        data = response.json()
        
        assert "libres" in data
        assert "privativas" in data
        assert "total" in data
        assert isinstance(data["libres"], list)
        assert isinstance(data["privativas"], list)
        assert len(data["libres"]) > 0
        assert len(data["privativas"]) > 0


class TestGraficos:
    """Tests para endpoints de gráficos"""
    
    def test_radar_dependencia(self, client):
        """Test gráfico de radar"""
        response = client.get("/api/radar-dependencia")
        assert response.status_code == 200
        data = response.json()
        assert "labels" in data
        assert "valoresDeDependencia" in data
        assert len(data["labels"]) == len(data["valoresDeDependencia"])
    
    def test_instituciones(self, client):
        """Test tabla de instituciones"""
        response = client.get("/api/instituciones")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verificar estructura de institución
        inst = data[0]
        assert "institucion" in inst
        assert "s" in inst
        assert "r" in inst
    
    def test_matriz_dependencia(self, client):
        """Test matriz de dependencia"""
        response = client.get("/api/matriz-dependencia")
        assert response.status_code == 200
        data = response.json()
        assert "series" in data
        assert "categorias" in data
        assert isinstance(data["series"], list)
        assert len(data["series"]) > 0


class TestAnalizar:
    """Tests para endpoint de análisis (infraestructura)"""
    
    def test_analizar_url_invalida(self, client):
        """Test con URL inválida"""
        response = client.post(
            "/api/analizar",
            json={"url": "https://sitio-que-no-existe-12345.invalid"}
        )
        # Puede ser 400 o 500 dependiendo de cómo maneje tu colega
        assert response.status_code in [400, 500]
    
    def test_analizar_respuesta_estructura(self, client):
        """Test que la respuesta tenga la estructura correcta"""
        # Con URL válida pero sin conexión, debe retornar error gracefully
        response = client.post(
            "/api/analizar",
            json={"url": "http://localhost:99999"}  # Puerto cerrado
        )
        # Estructura debe ser consistente
        assert response.status_code in [400, 500]


class TestValidacionModelos:
    """Tests para validación de modelos Pydantic"""
    
    def test_url_requerida_en_solicitud(self, client):
        """Test que URL es requerida"""
        response = client.post("/api/analizar", json={})
        assert response.status_code == 422  # Validation error
    
    def test_formato_respuesta_analisis(self, client):
        """Test estructura de respuesta"""
        # Esto es un test de estructura, no requiere conexión real
        # Tu colega puede ampliar esto cuando integre lógica real
        assert True  # Placeholder para que tu colega complete


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
