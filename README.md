# Microservicios con Docker - Sistema de Gestión de Usuarios y Tareas

## Descripción del Proyecto

Este proyecto implementa una arquitectura de microservicios completa para la gestión de usuarios y tareas, utilizando Docker, Docker Compose y Nginx Proxy Manager como API Gateway. El sistema incluye medidas de seguridad, alta disponibilidad y protección contra ataques DoS.

## Arquitectura

La aplicación está compuesta por los siguientes componentes:

- **user-service**: Microservicio para gestión de usuarios
- **task-service**: Microservicio para gestión de tareas
- **nginx-proxy-manager**: API Gateway con proxy inverso
- **SQLite**: Base de datos para persistencia

## Características Principales

### Seguridad
- **SSL/TLS**: Comunicación HTTPS con certificados válidos
- **Rate Limiting**: Protección contra ataques DoS (5 requests/segundo por IP)
- **Timeouts configurados**: Prevención de saturación del servidor
- **Límites de conexiones concurrentes**: Control de conexiones simultáneas

### Alta Disponibilidad
- **Réplicas múltiples**: Cada microservicio con al menos 2 réplicas
- **Balanceo de carga**: Distribución automática del tráfico
- **Health checks**: Monitoreo del estado de los servicios
- **Recuperación automática**: Tolerancia a fallos de instancias

### API Gateway
- **Enrutamiento centralizado**: Punto de entrada único
- **Proxy inverso**: Nginx Proxy Manager
- **Red interna segura**: Comunicación entre servicios

## Estructura del Proyecto

```
microservicios-proyecto/
├── user-service/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── database.db
├── task-service/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── database.db
├── nginx/
│   └── custom.conf
├── docker-compose.yml
└── README.md
```

## Instalación y Configuración

### Prerrequisitos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 1.29 o superior)
- Acceso a internet para descargar imágenes

### Configuración Inicial

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd microservicios-proyecto
   ```

2. **Construir y ejecutar los servicios**:
   ```bash
   docker-compose up --build -d
   ```

3. **Verificar que los servicios estén funcionando**:
   ```bash
   docker-compose ps
   ```

### Configuración del API Gateway

1. Acceder a Nginx Proxy Manager en: `http://localhost:81`
2. Credenciales por defecto:
   - Email: `admin@example.com`
   - Password: `changeme`
3. Configurar los proxy hosts para los servicios

## Endpoints de la API

### Servicio de Usuarios (`/api/users/`)

- `POST /api/users` - Registrar nuevo usuario
- `GET /api/users` - Listar todos los usuarios
- `GET /api/users/{id}` - Obtener usuario específico
- `GET /api/users/health` - Estado del servicio

### Servicio de Tareas (`/api/tasks/`)

- `POST /api/tasks` - Crear nueva tarea
- `GET /api/tasks` - Listar todas las tareas
- `GET /api/tasks/{id}` - Obtener tarea específica
- `PUT /api/tasks/{id}` - Actualizar estado de tarea
- `GET /api/tasks?user_id=X` - Filtrar tareas por usuario
- `GET /api/tasks/health` - Estado del servicio

### Estados de Tareas

- `pendiente` - Tarea creada pero no iniciada
- `en_progreso` - Tarea en desarrollo
- `completada` - Tarea finalizada

## Configuración de Seguridad

### Rate Limiting

El sistema implementa las siguientes medidas de protección:

```nginx
# Límite de requests por segundo
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;

# Límite de conexiones concurrentes
limit_conn_zone $binary_remote_addr zone=addr:10m;

# Timeouts de seguridad
client_header_timeout 10s;
client_body_timeout 10s;
send_timeout 10s;
```

### SSL/TLS

- Protocolo: TLS 1.2+
- Redirección automática HTTP → HTTPS
- Certificados válidos (Let's Encrypt recomendado)

## Pruebas de Resiliencia

### Pruebas de Carga

Ejecutar pruebas con Apache Benchmark:

```bash
# Prueba básica de carga
ab -n 1000 -c 10 https://localhost/api/users/

# Prueba con rate limiting
ab -n 100 -c 50 https://localhost/api/users/
```

### Pruebas de Disponibilidad

```bash
# Simular falla de una réplica
docker-compose stop user-service

# Verificar continuidad del servicio
curl https://localhost/api/users/health
```

## Monitoreo

### Health Checks

Cada servicio incluye health checks configurados:

```bash
# Verificar estado de todos los servicios
curl https://localhost/api/users/health
curl https://localhost/api/tasks/health
```

### Logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f user-service
```

## Desarrollo

### Variables de Entorno

El proyecto utiliza las siguientes variables de entorno:

```env
USER_SERVICE_PORT=5000
TASK_SERVICE_PORT=5001
NGINX_HTTP_PORT=80
NGINX_HTTPS_PORT=443
NGINX_ADMIN_PORT=81
```

### Escalado


## Solución de Problemas

### Problemas Comunes

1. **Servicios no se comunican**:
   - Verificar que estén en la misma red Docker
   - Comprobar nombres de servicios en docker-compose.yml

2. **Rate limiting muy restrictivo**:
   - Ajustar parámetros en `nginx/custom.conf`
   - Reiniciar nginx-proxy-manager

3. **SSL no funciona**:
   - Verificar configuración de certificados
   - Comprobar redirección HTTP → HTTPS

### Comandos Útiles

```bash
# Reiniciar todos los servicios
docker-compose restart

# Reconstruir servicios
docker-compose build --no-cache

# Limpiar recursos Docker
docker system prune -a
```

### Configuración Nginx Personalizada

El archivo `nginx/custom.conf` contiene la configuración avanzada para:
- Rate limiting
- Límites de conexiones
- Timeouts de seguridad
- Upstream para balanceo de carga

### Arquitectura de Red

```
Internet → Nginx Proxy Manager (Puerto 80/443)
                ↓
    Red interna (microservices_network)
                ↓
    user-service (múltiples réplicas)
    task-service (múltiples réplicas)
```
