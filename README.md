# Tiendas Online - Full Stack Application

Aplicación completa de tienda online con frontend en Angular 19, backend en Python con Flask, y base de datos MySQL (sin Docker).

## 🛒 Descripción del Proyecto

Sistema de gestión de tienda online que permite administrar usuarios con roles (admin/user), autenticación JWT y operaciones CRUD completas.

## 📋 Requisitos Previos

- **Node.js** 18+ y npm
- **Python** 3.8+
- **MySQL** 8.0+
- **Angular CLI** 19

## 🚀 Instalación y Ejecución (Sin Docker)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Leticia-Orive/frontend_backend_mysql.git
cd frontend_backend_mysql
```

### 2. Base de Datos MySQL

La base de datos se llama `tiendas_online`. Debes crearla manualmente.

#### Opción A: Desde la línea de comandos (PowerShell)

```powershell
# Ejecutar el script de inicialización (ajusta la ruta de mysql.exe según tu instalación):
Get-Content database\init.sql | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

#### Opción B: Usando MySQL Workbench

1. Abre MySQL Workbench
2. Conecta con tu servidor local (localhost)
3. Abre el archivo `database/init.sql`
4. Ejecuta el script completo (Ctrl + Shift + Enter)

#### Opción C: Desde MySQL CLI

```bash
mysql -u root -p < database\init.sql
```

### 3. Backend (Python Flask)

```powershell
cd backend

# Crear entorno virtual
py -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Edita el archivo .env y ajusta la contraseña de MySQL si es necesario:
# DB_PASSWORD=tu_contraseña_mysql

# Ejecutar servidor
py app.py
```

El backend estará disponible en: **http://localhost:5000**

### 4. Frontend (Angular 19)

Abre una nueva terminal:

```powershell
cd frontend

# Instalar dependencias (solo la primera vez)
npm install

# Ejecutar en modo desarrollo
npm start
```

El frontend estará disponible en: **http://localhost:4200**

## 📁 Estructura del Proyecto

```
frontend_backend_mysql/
├── backend/                 # Backend Python Flask
│   ├── app.py              # Aplicación principal con API REST
│   ├── requirements.txt    # Dependencias Python
│   ├── .env               # Configuración (DB: tiendas_online)
│   └── venv/              # Entorno virtual (creado al instalar)
├── database/              # Scripts de base de datos
│   └── init.sql          # Script de inicialización MySQL
├── frontend/             # Frontend Angular 19
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── login/      # Componente de login
│   │   │   │   ├── register/   # Componente de registro
│   │   │   │   └── user-list/  # Componente lista de usuarios
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts  # Guardia de autenticación
│   │   │   ├── models/
│   │   │   │   └── user.model.ts  # Modelo de usuario
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts  # Servicio de autenticación
│   │   │   │   └── user.service.ts  # Servicio de usuarios
│   │   │   ├── app.component.ts
│   │   │   ├── app.config.ts
│   │   │   └── app.routes.ts
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.css
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
└── README.md             # Este archivo
```

## 🔑 Usuarios de Prueba

Después de ejecutar el script `init.sql`, tendrás estos usuarios de prueba:

| Email | Password | Rol |
|-------|----------|-----|
| admin@example.com | 123456 | admin |
| juan.perez@example.com | 123456 | user |
| maria.garcia@example.com | 123456 | user |
| carlos.lopez@example.com | 123456 | user |
| ana.martinez@example.com | 123456 | user |

## 🔌 API Endpoints

### Autenticación
- **POST** `/api/register` - Registrar nuevo usuario
- **POST** `/api/login` - Iniciar sesión

### Usuarios (Requieren autenticación)
- **GET** `/api/users` - Listar todos los usuarios
- **GET** `/api/users/{id}` - Obtener un usuario por ID
- **PUT** `/api/users/{id}` - Actualizar un usuario
- **DELETE** `/api/users/{id}` - Eliminar un usuario

## ⚙️ Configuración

### Backend (.env)

El archivo `backend/.env` contiene la configuración de la base de datos:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=          # Ajusta según tu configuración
DB_NAME=tiendas_online
DB_PORT=3306
JWT_SECRET=mi_clave_secreta_super_segura_123456
```

**IMPORTANTE**: Ajusta `DB_PASSWORD` con la contraseña de tu usuario root de MySQL.

### Frontend

El frontend está configurado para conectarse al backend en `http://localhost:5000`.
Si cambias el puerto del backend, actualiza las URLs en los servicios de Angular.

## 🛠️ Tecnologías Utilizadas

### Frontend
- Angular 19
- TypeScript 5.6
- RxJS 7.8
- Angular Router
- HTTP Client

### Backend
- Python 3.x
- Flask 3.0
- PyMySQL 1.1
- Flask-CORS 4.0
- PyJWT 2.8
- bcrypt 4.1
- python-dotenv 1.0

### Base de Datos
- MySQL 8.0

## 🐛 Solución de Problemas

### El backend no conecta con MySQL

1. Verifica que MySQL esté ejecutándose:
   ```powershell
   Get-Service MySQL80  # O el nombre de tu servicio MySQL
   ```

2. Verifica las credenciales en `backend/.env`

3. Asegúrate de que la base de datos `tiendas_online` existe:
   ```sql
   SHOW DATABASES;
   ```

### Error al instalar dependencias de Python

Si tienes problemas con bcrypt o cryptography:
```powershell
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt
```

### El frontend no se conecta al backend

1. Verifica que el backend esté corriendo en http://localhost:5000
2. Verifica la consola del navegador para errores CORS
3. Asegúrate de que Flask-CORS esté instalado correctamente

## 📝 Notas

- Este proyecto NO usa Docker, todo se ejecuta de forma nativa en Windows
- Asegúrate de tener MySQL instalado y corriendo antes de iniciar el backend
- El backend usa variables de entorno del archivo `.env`
- La contraseña por defecto de todos los usuarios de prueba es `123456`

## 📧 Contacto

Para preguntas o sugerencias, contacta a: Leticia Orive
