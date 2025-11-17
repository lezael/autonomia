# 🔒 GUÍA DE SEGURIDAD - AutonomIA

## Estado: ✅ 100% IMPLEMENTADO

Se han implementado **6 medidas de seguridad críticas** para proteger la API contra:
- Ataques DoS (Denegación de Servicio)
- SSRF (Server-Side Request Forgery)
- Acceso no autorizado
- Exhaustión de recursos
- Inyección de contenido malicioso

---

## 1️⃣ INSTALACIÓN DE DEPENDENCIAS

Los paquetes de seguridad ya están en `requisitos.txt`:

```bash
cd backend_python
pip install -r requisitos.txt
```

**Nuevas dependencias agregadas:**
- `slowapi==0.1.5` - Rate limiting
- `python-dotenv==0.19.0` - Gestión de variables de entorno
- `ipaddress>=1.0.23` - Validación de IPs

---

## 2️⃣ CONFIGURACIÓN INICIAL

### Opción A: Desarrollo (Sin Autenticación)

```bash
cd backend_python
# Simplemente iniciar el servidor
python -m uvicorn main:app --reload
# El servidor operará sin require API key
```

### Opción B: Producción (Con Autenticación)

```bash
cd backend_python

# Paso 1: Generar configuración segura
python generar_configuracion.py
# Sigue las indicaciones interactivas
# Esto crea un archivo .env con API key aleatoria

# Paso 2: Verificar que .env se creó
cat .env
# Deberías ver: API_KEY=<clave-aleatoria>

# Paso 3: Iniciar servidor
python -m uvicorn main:app --host 0.0.0.0 --port 8000
# Ahora la API requiere X-API-Key header
```

---

## 3️⃣ MEDIDAS DE SEGURIDAD IMPLEMENTADAS

### 🔴 Medida 1: Rate Limiting
**Ubicación:** `main.py` - Decorador `@limiter.limit()`

```python
@app.post("/analizar")
@limiter.limit("5/minute")  # Máximo 5 solicitudes por minuto
async def analizar_url(...):
    ...
```

**Beneficio:** Previene ataques de fuerza bruta y DoS
**Límites:**
- `/analizar`: 5 solicitudes/minuto/IP
- `/tecnologias`: 30 solicitudes/minuto/IP

**Respuesta si se excede:**
```json
{
  "estado": "error",
  "mensaje": "Demasiadas solicitudes. Máximo 5 solicitudes por minuto.",
  "código": 429
}
```

---

### 🔐 Medida 2: Autenticación por API Key
**Ubicación:** `main.py` - Función `validar_api_key()`

**Uso desde cliente:**
```bash
# Con API key (producción)
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: tu-api-key-aqui" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ejemplo.com"}'

# Sin API key (desarrollo)
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ejemplo.com"}'
```

**Respuesta sin API key (en producción):**
```json
{
  "detail": "API key requerida"
}
```

**Respuesta con API key incorrecta:**
```json
{
  "detail": "API key inválida"
}
```

---

### 🛡️ Medida 3: SSRF Protection (Validación de URL)
**Ubicación:** `app/utilidades/validadores.py` - Función `validar_url_segura()`

**Bloquea:**
- ✗ Localhost: `http://127.0.0.1`, `http://[::1]`
- ✗ IPs privadas: `192.168.*`, `10.*`, `172.16-31.*`
- ✗ Link-local: `169.254.*`
- ✗ Reservadas: `0.0.0.0`, etc.

**Permite:**
- ✓ Dominios públicos: `https://google.com`
- ✓ IPs públicas: `http://8.8.8.8`

**Ejemplo de bloqueo:**
```bash
# URL bloqueada
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://192.168.1.1"}'
  
# Respuesta: 400 Bad Request
# "No se permiten IPs privadas"
```

---

### 📄 Medida 4: Content-Type Validation
**Ubicación:** `app/extraccion/manejador_peticiones.py`

**Solo acepta:** `text/html`
**Rechaza:** Binarios, PDFs, imágenes, JSON, etc.

**Validación:**
```python
content_type = response.headers.get('content-type', '').lower()
if 'text/html' not in content_type:
    return False, None, "Tipo de contenido no permitido"
```

---

### 💾 Medida 5: Límite de Tamaño de Descarga
**Ubicación:** `app/extraccion/manejador_peticiones.py`

**Máximo:** 10 MB (10,485,760 bytes)

**Validación en dos niveles:**
1. Verificar header `Content-Length` antes de descargar
2. Contar bytes durante la descarga (stream)

```python
MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Si Content-Length > 10MB → rechaza
# Si stream supera 10MB durante descarga → rechaza
```

**Error si excede:**
```json
{
  "detail": "No se pudo acceder a la URL: Archivo demasiado grande"
}
```

---

### 🔗 Medida 6: Restricción de Protocolos
**Ubicación:** `app/utilidades/validadores.py`

**Solo permite:**
- ✓ `http://`
- ✓ `https://`

**Rechaza:**
- ✗ `ftp://`
- ✗ `file://`
- ✗ `gopher://`
- ✗ Cualquier otro protocolo

**Validación:**
```python
if parsed.scheme not in ('http', 'https'):
    return False, "Solo se permiten URLs HTTP/HTTPS"
```

---

## 4️⃣ PRUEBAS DE SEGURIDAD

### Test 1: Verificar Rate Limiting
```bash
# Hacer 7 solicitudes en rápida sucesión
for i in {1..7}; do
  curl -X GET "http://localhost:8000/salud"
  echo "Solicitud $i"
done

# Resultado esperado:
# Solicitudes 1-5: 200 OK
# Solicitudes 6-7: 429 Too Many Requests
```

### Test 2: Verificar SSRF Blocking
```bash
# Intentar acceder a localhost
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://127.0.0.1:5000"}'

# Respuesta esperada: 400 Bad Request
# "No se pueden analizar URLs locales"
```

### Test 3: Verificar API Key en Producción
```bash
# Sin API key
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta: 403 Forbidden (si API_KEY está configurada)

# Con API key incorrecta
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: wrong-key" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta: 403 Forbidden

# Con API key correcta
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: <tu-api-key>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
# Respuesta: 200 OK con análisis
```

### Test 4: Verificar Content-Type
```bash
# URL que devuelve PDF (no HTML)
curl -X POST "http://localhost:8000/analizar" \
  -H "X-API-Key: dev-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/documento.pdf"}'
# Respuesta: 400 Bad Request - "Tipo de contenido no permitido"
```

### Test 5: Verificar Size Limit
```bash
# Crear un servidor de prueba que devuelve >10MB
# El análisis debería fallar por exceso de tamaño
```

---

## 5️⃣ MONITOREO Y LOGS

### Ubicación de Logs
```
logs/autonomia.log
```

### Eventos de Seguridad Registrados
```
[RATE_LIMIT] Rate limit excedido para IP X.X.X.X
[AUTH_FAILED] Intento sin API key / API key inválida
[SSRF_BLOCK] URL rechazada por seguridad - razón
[CONTENT_TYPE] Tipo de contenido no permitido
[SIZE_LIMIT] Archivo excede límite de 10MB
[PROTOCOL] Protocolo no permitido
```

### Lectura de Logs
```bash
# Últimas 20 líneas
tail -20 logs/autonomia.log

# Ver solo errores de seguridad
grep -i "SSRF\|rate\|auth\|forbidden" logs/autonomia.log

# Seguimiento en tiempo real
tail -f logs/autonomia.log
```

---

## 6️⃣ RECOMENDACIONES PARA PRODUCCIÓN

### Nivel CRÍTICO 🔴
1. **Cambiar API Key periódicamente**
   - Cada 90 días mínimo
   - Usar: `python generar_configuracion.py`

2. **Guardar .env en lugar seguro**
   - NO commitar a Git
   - Usar variables de entorno del servidor
   - Permisos: 600 (solo propietario)

3. **Usar HTTPS obligatorio**
   - Cambiar `allow_origins` a dominios específicos
   - Implementar certificados SSL/TLS
   - Redirigir HTTP → HTTPS

### Nivel IMPORTANTE 🟡
4. **Monitoreo de alertas**
   - Alerta si múltiples 429 desde una IP
   - Alerta si múltiples 403 (intentos de auth fallidos)
   - Alerta si bloqueos SSRF sospechosos

5. **Rotación de logs**
   - Mantener 30 días mínimo
   - Archivar logs antiguos
   - Análisis periódico

6. **Firewall y Rate Limit en infraestructura**
   - Limitar conexiones por IP a nivel de firewall
   - Usar CDN con protección DDoS
   - Implementar WAF (Web Application Firewall)

### Nivel RECOMENDADO 🟢
7. **Headers de Seguridad HTTP**
   ```python
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
   Strict-Transport-Security: max-age=31536000
   ```

8. **Validación adicional**
   - Implementar CAPTCHA para rate limit excedido
   - Usar verificación de dos factores para admin panel
   - Logging de todas las acciones

---

## 7️⃣ CHECKLIST DE SEGURIDAD

Antes de desplegar a producción:

- [ ] Archivo .env creado con API Key
- [ ] .env incluido en .gitignore
- [ ] Requisitos instalados: `pip install -r requisitos.txt`
- [ ] Rate limiting activo (verificar con test)
- [ ] SSRF protection activo (bloquea 127.0.0.1)
- [ ] Autenticación activa (X-API-Key requerida)
- [ ] Logs siendo generados correctamente
- [ ] Content-Type validation activo
- [ ] Size limit (10MB) funcionando
- [ ] CORS restrictivo (dominios específicos, no *)
- [ ] HTTPS habilitado en servidor
- [ ] Certificado SSL válido
- [ ] Monitoreo de errores configurado
- [ ] Backups de logs configurados
- [ ] Documentación compartida con equipo

---

## 8️⃣ CONTACTO Y SOPORTE

**Problemas comunes:**

**P: "403 Forbidden - API key requerida"**
R: Agregar header `X-API-Key: <tu-clave>` a todas las solicitudes

**P: "429 Too Many Requests"**
R: Normal - esperar 1 minuto o cambiar IP. Contactar si es legítimo uso

**P: "No se permiten IPs privadas"**
R: Las URLs debe apuntar a servidores públicos. No se pueden analizar máquinas locales

**P: "Tipo de contenido no permitido"**
R: Solo se aceptan URLs que devuelven `text/html`. Verificar URL

**P: "Archivo demasiado grande"**
R: Página web > 10MB. Contactar si es necesario aumentar límite

---

**Última actualización:** 2024-01-15
**Versión:** 1.0.0 - Seguridad Completa
