"""Manejador de peticiones HTTP con timeouts, seguridad y manejo de errores."""
import requests
from typing import Optional, Tuple
from requests.exceptions import Timeout, ConnectionError, RequestException
from app.utilidades.logger_config import logger_app


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TIMEOUT_SEGUNDOS = 10
MAX_REDIRECTS = 5
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def obtener_contenido_url(url: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Obtiene el contenido HTML de una URL con manejo robusto de errores y validaciones de seguridad.
    
    Args:
        url: URL a acceder
    
    Returns:
        Tupla (éxito, contenido_html, mensaje_error)
    """
    try:
        logger_app.info(f"Accediendo a URL: {url}")
        
        # Usar stream=True para validar Content-Length antes de descargar
        response = requests.get(
            url,
            timeout=TIMEOUT_SEGUNDOS,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
            stream=True,
        )
        
        # Validar código de estado
        if response.status_code == 403:
            mensaje = "Acceso denegado (403) - Servidor rechazó la solicitud"
            logger_app.warning(f"{url}: {mensaje}")
            return False, None, mensaje
        elif response.status_code == 404:
            mensaje = "Página no encontrada (404)"
            logger_app.warning(f"{url}: {mensaje}")
            return False, None, mensaje
        elif response.status_code >= 500:
            mensaje = f"Error del servidor ({response.status_code})"
            logger_app.error(f"{url}: {mensaje}")
            return False, None, mensaje
        elif response.status_code >= 400:
            mensaje = f"Error HTTP ({response.status_code})"
            logger_app.warning(f"{url}: {mensaje}")
            return False, None, mensaje
        
        # Validar Content-Type - Solo HTML
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            mensaje = f"Tipo de contenido no permitido: {content_type}. Solo se acepta text/html"
            logger_app.warning(f"{url}: {mensaje}")
            response.close()
            return False, None, mensaje
        
        # Validar Content-Length si existe
        content_length = response.headers.get('content-length')
        if content_length:
            try:
                size = int(content_length)
                if size > MAX_SIZE_BYTES:
                    mensaje = f"Archivo demasiado grande: {size} bytes > {MAX_SIZE_BYTES} bytes (10 MB)"
                    logger_app.warning(f"{url}: {mensaje}")
                    response.close()
                    return False, None, mensaje
            except ValueError:
                logger_app.warning(f"{url}: Content-Length inválido: {content_length}")
        
        # Descargar con límite de tamaño
        content = b""
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                content += chunk
                if len(content) > MAX_SIZE_BYTES:
                    mensaje = f"Descarga excedió el límite de {MAX_SIZE_BYTES} bytes"
                    logger_app.warning(f"{url}: {mensaje}")
                    response.close()
                    return False, None, mensaje
        
        response.close()
        
        if len(content) == 0:
            mensaje = "Respuesta vacía del servidor"
            logger_app.warning(f"{url}: {mensaje}")
            return False, None, mensaje
        
        # Decodificar con manejo de errores
        try:
            html_content = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                html_content = content.decode('latin-1')
            except UnicodeDecodeError:
                html_content = content.decode('utf-8', errors='ignore')
        
        logger_app.info(f"URL accedida exitosamente: {url} ({len(content)} bytes)")
        return True, html_content, None
        
    except Timeout:
        mensaje = f"Timeout - No se obtuvo respuesta en {TIMEOUT_SEGUNDOS} segundos"
        logger_app.error(f"{url}: {mensaje}")
        return False, None, mensaje
        
    except ConnectionError as e:
        mensaje = f"Error de conexión: {str(e)}"
        logger_app.error(f"{url}: {mensaje}")
        return False, None, mensaje
        
    except RequestException as e:
        mensaje = f"Error en la solicitud: {str(e)}"
        logger_app.error(f"{url}: {mensaje}")
        return False, None, mensaje
        
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
        logger_app.error(f"{url}: {mensaje}")
        return False, None, mensaje


def validar_accesibilidad_url(url: str) -> Tuple[bool, str]:
    """
    Valida que una URL es accesible sin descargar contenido completo.
    
    Args:
        url: URL a validar
    
    Returns:
        Tupla (es_accesible, mensaje)
    """
    try:
        response = requests.head(
            url,
            timeout=5,
            headers={"User-Agent": USER_AGENT},
            allow_redirects=True,
        )
        
        if response.status_code < 400:
            return True, "URL accesible"
        else:
            return False, f"Error HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
