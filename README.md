# Microservicios con Alta Disponibilidad, Seguridad y Orquestación

Este proyecto implementa una arquitectura basada en microservicios, con servicios separados para la gestión de usuarios y tareas, utilizando un API Gateway seguro (Nginx Proxy Manager), contenedores Docker y orquestación con Docker Compose. También incluye mecanismos para mitigar ataques de denegación de servicio (DoS) y mejorar la resiliencia del sistema mediante réplicas.

---

## Arquitectura de la Aplicación

### Componentes principales:
- **🔐 user-service**: Gestión de usuarios del sistema (registro, consulta y validación).
- **✅ task-service**: Manejo de tareas asignadas a usuarios.
- **🌐 API Gateway (nginx-proxy)**: Enrutamiento seguro del tráfico hacia los microservicios.

---

## 📦 Servicios

### 1. user-service

Gestor de información de usuarios.

- **Tecnologías**: Python + Flask + SQLite
- **Endpoints REST**:
  - `POST /users` - Registrar un nuevo usuario
  - `GET /users` - Listar todos los usuarios
  - `GET /users/{id}` - Obtener usuario específico
  - `GET /health` - Verificación de estado
- **Validaciones**:
  - Campos obligatorios
  - Email único y formato válido
- **Contenerización**:
  - Dockerfile optimizado
- **Persistencia**:
  - Base de datos SQLite local

---

### 2. task-service

Gestor de tareas con validación de usuarios.

- **Tecnologías**: Python + Flask + SQLite
- **Endpoints REST**:
  - `POST /tasks` - Crear nueva tarea
  - `GET /tasks` - Listar todas las tareas
  - `GET /tasks/{id}` - Obtener tarea específica
  - `PUT /tasks/{id}` - Actualizar tarea
  - `GET /tasks?user_id=X` - Tareas por usuario
  - `GET /health` - Verificación de estado
- **Estados**: `pendiente`, `en progreso`, `completada`
- **Relaciones**: Tareas vinculadas a usuarios mediante IDs
- **Contenerización**:
  - Dockerfile para construcción de imagen

---

## 🧪 Orquestación con Docker Compose

Archivo `docker-compose.yml` que:

- Define los servicios: `user-service`, `task-service`
- Configura red interna para comunicación segura
- Define API Gateway con [Nginx Proxy Manager](https://nginxproxymanager.com/)
- Expone rutas:
  - `/api/users/*` → user-service
  - `/api/tasks/*` → task-service
  - `/admin` → Interfaz de NPM
- Configura:
  - Volúmenes persistentes
  - Variables de entorno
  - Health checks
  - Réplicas para alta disponibilidad

---

## 🔐 Seguridad y Alta Disponibilidad

### 1. API Gateway Seguro

- **HTTPS activado con certificados SSL/TLS**
  - Generados con Let's Encrypt (Certbot) o OpenSSL (autofirmado)
- **Redirección automática de HTTP → HTTPS**
- **Cifrado robusto (TLS 1.2+)**

📸 *Evidencia: Navegador mostrando conexión segura*

---

### 2. Defensa ante ataques DoS (Denegación de Servicio)

- **Simulación de ataques**:
  - Herramientas: `slowhttptest`, `ab`
  - Análisis de logs y comportamiento
- **Mitigaciones implementadas**:
  - `Rate limiting` (límites por IP)
  - Timeouts en Nginx
  - Límites de conexiones simultáneas
  - Monitoreo de recursos

📸 *Comparativa de logs antes y después de mitigar*

📖 *Análisis teórico de detección de ataques DoS en entornos reales*

---

### 3. Alta Disponibilidad

- **Réplicas**:
  - Mínimo 2 réplicas por microservicio
  - Balanceo de carga con Nginx Proxy
- **Pruebas**:
  - Falla controlada de un contenedor
  - Verificación de continuidad de servicio
  - Evaluación del tiempo de recuperación

📸 *Logs mostrando continuidad y resiliencia bajo carga*

---

## ▶️ Cómo ejecutar

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/nombre-del-proyecto.git
cd nombre-del-proyecto

# Construir e iniciar servicios
docker-compose up --build
