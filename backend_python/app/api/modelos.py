"""
Modelos Pydantic para validación de datos en la API.
Tu colega extenderá estos modelos con lógica de análisis específica.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum


class TipoTecnologia(str, Enum):
    """Tipos de tecnologías detectadas"""
    LIBRE = "libre"
    PRIVATIVO = "privativo"
    MIXTO = "mixto"


class Tecnologia(BaseModel):
    """Modelo para una tecnología detectada"""
    nombre: str = Field(..., description="Nombre de la tecnología")
    tipo: TipoTecnologia = Field(..., description="Clasificación: libre/privativo/mixto")
    confianza: float = Field(default=0.85, ge=0.0, le=1.0, description="Nivel de confianza 0-1")
    categoria: Optional[str] = Field(default=None, description="Categoría: Analítica, CMS, etc")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Google Analytics",
                "tipo": "privativo",
                "confianza": 0.95,
                "categoria": "Analítica"
            }
        }


class SolicitudAnalisis(BaseModel):
    """Modelo para solicitud de análisis de URL"""
    url: HttpUrl = Field(..., description="URL de la institución a analizar")
    
    class Config:
        json_schema_extra = {
            "example": {"url": "https://www.universidad.edu.py"}
        }


class ResultadoAnalisis(BaseModel):
    """Modelo para resultado de análisis"""
    url: str = Field(..., description="URL analizada")
    
    # Métricas (tu colega completará la lógica)
    indice_soberania: Optional[float] = Field(
        default=None, 
        ge=0.0, 
        le=1.0,
        description="Índice S(i): 0 (100% dependiente) a 1 (100% soberano)"
    )
    ranking_normalizado: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Ranking R(i) normalizado 0-1 (multiplicar por 10 para escala 0-10)"
    )
    
    # Tecnologías detectadas
    tecnologias_detectadas: List[Tecnologia] = Field(
        default_factory=list,
        description="Lista de tecnologías encontradas"
    )
    tecnologias_libres_count: int = Field(default=0, description="Cantidad de tecnologías libres")
    tecnologias_privativas_count: int = Field(default=0, description="Cantidad de tecnologías privativas")
    
    # Matriz de dependencia (tu colega completará)
    matriz_dependencia: Optional[List[List[int]]] = Field(
        default=None,
        description="Matriz D de dependencia (n_tech x propiedades)"
    )
    
    # Recomendaciones
    recomendaciones: List[str] = Field(default_factory=list, description="Sugerencias personalizadas")
    
    # Estado
    estado: str = Field(default="éxito", description="éxito, error, procesando")
    mensaje: str = Field(default="Análisis completado", description="Mensaje descriptivo")
    tiempo_procesamiento_ms: Optional[int] = Field(default=None, description="Milisegundos de procesamiento")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.universidad.edu.py",
                "indice_soberania": 0.65,
                "ranking_normalizado": 0.65,
                "tecnologias_detectadas": [
                    {
                        "nombre": "Google Analytics",
                        "tipo": "privativo",
                        "confianza": 0.95,
                        "categoria": "Analítica"
                    }
                ],
                "tecnologias_libres_count": 2,
                "tecnologias_privativas_count": 5,
                "recomendaciones": ["Considerar Matomo como alternativa libre"],
                "estado": "éxito",
                "mensaje": "Análisis completado exitosamente",
                "tiempo_procesamiento_ms": 2500
            }
        }


class RespuestaSalud(BaseModel):
    """Modelo para health check"""
    status: str = Field(description="Estado del servidor")
    version: str = Field(description="Versión de la API")
    mensaje: str = Field(default="API operacional")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "operacional",
                "version": "1.0.0",
                "mensaje": "API operacional"
            }
        }


class ListaTecnologias(BaseModel):
    """Modelo para listar tecnologías disponibles"""
    libres: List[str] = Field(description="Tecnologías libres")
    privativas: List[str] = Field(description="Tecnologías privativas")
    total: int = Field(description="Total de tecnologías")
    
    class Config:
        json_schema_extra = {
            "example": {
                "libres": ["Moodle", "WordPress", "Nextcloud"],
                "privativas": ["Google Analytics", "Microsoft Azure"],
                "total": 5
            }
        }


class DatosRadar(BaseModel):
    """Modelo para datos de gráfico radar"""
    labels: List[str] = Field(description="Etiquetas de servicios")
    valoresDeDependencia: List[int] = Field(description="Valores de dependencia")
    
    class Config:
        json_schema_extra = {
            "example": {
                "labels": ["Google", "AWS", "Microsoft", "Meta"],
                "valoresDeDependencia": [2, 1, 2, 1]
            }
        }


class DatosTablaInstituciones(BaseModel):
    """Modelo para tabla de instituciones"""
    institucion: str
    s: float = Field(description="Índice de soberanía")
    r: float = Field(description="Ranking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "institucion": "Univ_A",
                "s": -25,
                "r": 3.5
            }
        }


class SerieHeatmap(BaseModel):
    """Modelo para serie de heatmap"""
    name: str
    data: List[int]


class DatosMatrizDependencia(BaseModel):
    """Modelo para datos de matriz de dependencia"""
    series: List[SerieHeatmap]
    categorias: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "series": [
                    {"name": "Univ_A", "data": [1, 0, 1, 0]},
                    {"name": "Univ_B", "data": [1, 1, 0, 0]}
                ],
                "categorias": ["Google", "AWS", "Microsoft", "Meta"]
            }
        }
