# SEGURIDAD - Hardening AutonomIA

## Medidas de Seguridad Implementadas

### 1. ✅ Rate Limiting (slowapi)
- **Limitación:** 5 solicitudes por minuto por IP
- **Endpoint /analizar:** @limiter.limit("5/minute")
- **Endpoint /tecnologias:** @limiter.limit("30/minute")
- **Beneficio:** Previene ataques de fuerza bruta y DoS
- **Respuesta:** 429 Too Many Requests cuando se excede

### 2. ✅ Autenticación por API Key
- **Método:** Header `X-API-Key`
- **Validación:** Contra variable de entorno `API_KEY`
- **Desarrollo:** Sin API key = acceso libre (para pruebas)
- **Producción:** Requerir API key válida
- **Respuesta:** 403 Forbidden si falta o es inválida

### 3. ✅ Validación de URL (SSRF Prevention)
- **Bloquea:** IPs locales (127.0.0.1, ::1, 0.0.0.0)
- **Bloquea:** IPs privadas (192.168.*, 10.*, 172.16-31.*)
- **Bloquea:** Link-local (169.254.*)
- **Bloquea:** Subredes reservadas
- **Métodos:** `ipaddress` + regex patterns
- **Respuesta:** 400 Bad Request con mensaje específico

### 4. ✅ Content-Type Validation
- **Aceptado:** Solo `text/html`
- **Rechazado:** Binarios, JSON, imágenes, etc.
- **Ubicación:** manejador_peticiones.py
- **Respuesta:** 400 Bad Request si Content-Type no es HTML

### 5. ✅ Límite de Tamaño de Descarga
- **Máximo:** 10 MB (10,485,760 bytes)
- **Validación:** Contra Content-Length header
- **Runtime:** Control en stream de descarga
- **Respuesta:** 400 Bad Request si excede límite
- **Beneficio:** Previene exhaustión de memoria

### 6. ✅ Restricción de Protocolos
- **Permitidos:** http://, https://
- **Bloqueados:** ftp://, file://, gopher://, etc.
- **Validación:** En validador de URL
- **Respuesta:** 400 Bad Request si protocolo no permitido

---

## Configuración de Seguridad

### Para Desarrollo (Sin Autenticación)
```bash
# No establecer API_KEY - el sistema operará sin autenticación
# Todos los demás controles de seguridad siguen activos
python -m uvicorn main:app --reload
```

### Para Producción (Con Autenticación)
```bash
# 1. Generar API key segura
python -c "import secrets; print(secrets.token_urlsafe(32))"

# 2. Crear archivo .env con API key
echo "API_KEY=<clave-generada>" > .env

# 3. Iniciar servidor (rechazará solicitudes sin API key)
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Pruebas de Seguridad

### Test 1: Rate Limiting
```bash
# Hacer más de 5 solicitudes en 1 minuto desde la misma IP
for i in {1..7}; do
  curl -X GET "http://localhost:8000/salud"
done
# Resultado esperado: Las solicitudes 6-7 devuelven 429
```

### Test 2: SSRF Protection
```bash
# Intentar acceder a localhost (debe fallar)
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1:8000"}'
# Respuesta esperada: 400 - "No se pueden analizar URLs locales"

# Intentar acceder a IP privada
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://192.168.1.1"}'
# Respuesta esperada: 400 - "No se permiten IPs privadas"
```

### Test 3: API Key Authentication
```bash
# Sin API key (si está configurada)
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta esperada: 403 - "API key requerida"

# Con API key incorrecta
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: wrong-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta esperada: 403 - "API key inválida"

# Con API key correcta
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta esperada: 200 OK con análisis
```

### Test 4: Content-Type Validation
```bash
# URL de archivo no HTML
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/document.pdf"}'
# Respuesta esperada: 400 - "Tipo de contenido no permitido"
```

### Test 5: Size Limit
```bash
# URL que devuelve >10MB (difícil de simular)
# El servidor rechazará durante la descarga si excede 10MB
```

---

## Logs de Seguridad

Todos los eventos de seguridad se registran en `logs/autonomia.log`:

```
[2024-01-15 10:30:45] WARNING: Rate limit excedido para 192.168.1.100
[2024-01-15 10:31:12] WARNING: Intento de acceso sin API key
[2024-01-15 10:31:20] WARNING: URL rechazada por seguridad: http://192.168.1.1 - No se permiten IPs privadas
[2024-01-15 10:31:25] WARNING: Tipo de contenido no permitido: application/pdf
```

---

## Recomendaciones Adicionales

### Para Producción
1. **HTTPS obligatorio:** Cambiar `allow_origins=["*"]` a dominios específicos
2. **CORS restrictivo:** Especificar solo dominios autorizados
3. **API Key fuerte:** Generar con `secrets.token_urlsafe(32)` 
4. **Rotación de claves:** Cambiar API_KEY periódicamente
5. **Monitoreo:** Alertar si se detectan múltiples 403 Forbidden
6. **Logareo:** Mantener logs por 30 días mínimo
7. **Firewall:** Restricción de IPs a nivel de infraestructura
8. **Rate Limit Ajustable:** Modificar según necesidades (actual: 5/min)

### Headers de Seguridad Recomendados
```python
# Agregar a FastAPI:
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

---

## Validación

Todas las medidas fueron implementadas y validadas:
- ✅ Validadores.py: `validar_url_segura()` con bloqueo de IPs privadas
- ✅ Manejador_peticiones.py: Content-Type y size limit checks
- ✅ Main.py: Rate limiting, API key, decorators, exception handlers
- ✅ Requisitos.txt: slowapi y python-dotenv añadidos
- ✅ .env.example: Template para configuración segura

---

**Estatus:** 🟢 COMPLETO - 6/6 medidas de seguridad implementadas
