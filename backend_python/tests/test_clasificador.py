"""Test del clasificador de tecnologías"""
import pytest
from app.extraccion.clasificador_tecnologias import (
    clasificar_tecnologia,
    categorizar_tecnologias,
    calcular_indice_soberania,
    calcular_ranking_normalizado,
    obtener_recomendaciones
)


class TestClasificadorTecnologias:
    """Tests para el módulo clasificador_tecnologias"""
    
    def test_clasificar_tecnologia_libre(self):
        """Test clasificación de tecnología libre"""
        resultado = clasificar_tecnologia("Nextcloud", "libre")
        assert resultado["tipo"] == "libre"
        assert resultado["clasificacion"] == "Libre"
        assert "abierto" in resultado["descripcion"].lower()
    
    def test_clasificar_tecnologia_privativa(self):
        """Test clasificación de tecnología privativa"""
        resultado = clasificar_tecnologia("Google Analytics", "privativo")
        assert resultado["tipo"] == "privativo"
        assert resultado["clasificacion"] == "Privativo"
    
    def test_categorizar_tecnologias(self):
        """Test categorización de tecnologías"""
        techs = [
            {"nombre": "WordPress", "tipo": "libre"},
            {"nombre": "Google Analytics", "tipo": "privativo"},
            {"nombre": "Nextcloud", "tipo": "libre"},
        ]
        
        resultado = categorizar_tecnologias(techs)
        assert resultado["total_libres"] == 2
        assert resultado["total_privativas"] == 1
        assert resultado["total"] == 3
    
    def test_calcular_indice_soberania(self):
        """Test cálculo del índice de soberanía"""
        # 2 libres, 2 privativas = 50%
        indice = calcular_indice_soberania(2, 2)
        assert indice == 0.5
        
        # 3 libres, 1 privativa = 75%
        indice = calcular_indice_soberania(3, 1)
        assert indice == 0.75
        
        # 0 libres, 0 privativas = 0%
        indice = calcular_indice_soberania(0, 0)
        assert indice == 0.0
    
    def test_calcular_ranking_normalizado(self):
        """Test cálculo del ranking normalizado"""
        # 50% = 5.0
        ranking = calcular_ranking_normalizado(0.5)
        assert ranking == 0.5
        
        # 100% = 10.0
        ranking = calcular_ranking_normalizado(1.0)
        assert ranking == 1.0
        
        # 0% = 0.0
        ranking = calcular_ranking_normalizado(0.0)
        assert ranking == 0.0
    
    def test_obtener_recomendaciones_alto_privativo(self):
        """Test recomendaciones con alto nivel de privativo"""
        techs = [
            {"nombre": "Google Analytics"},
            {"nombre": "Microsoft Azure"},
            {"nombre": "AWS CloudFront"},
            {"nombre": "Facebook Pixel"},
            {"nombre": "Google Fonts"},
            {"nombre": "LinkedIn Insight"},
        ]
        
        recomendaciones = obtener_recomendaciones(techs)
        assert len(recomendaciones) > 0
        # Debe incluir alerta de alto nivel de dependencia
        assert any("auditoría" in r.lower() or "dependencia" in r.lower() 
                  for r in recomendaciones)
    
    def test_obtener_recomendaciones_bajo_privativo(self):
        """Test recomendaciones con bajo nivel de privativo"""
        techs = [
            {"nombre": "Google Analytics"},
        ]
        
        recomendaciones = obtener_recomendaciones(techs)
        assert len(recomendaciones) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
