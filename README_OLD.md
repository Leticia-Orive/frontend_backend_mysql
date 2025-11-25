# Tienda Online - Full Stack Application

Aplicación completa de tienda online con frontend en Angular 19, backend en Python con Flask, y base de datos MySQL.

## 🛒 Descripción del Proyecto

Sistema de gestión de tienda online que permite administrar usuarios, productos y pedidos.

## 📋 Requisitos Previos

- **Node.js** 18+ y npm
- **Python** 3.8+
- **MySQL** 8.0+
- **Angular CLI** 19

## 🚀 Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Leticia-Orive/frontend_backend_mysql.git
cd frontend_backend_mysql
```

### 2. Base de Datos MySQL

La base de datos se llama `tienda_online` y ya está configurada.

```bash
# Ejecutar el script de inicialización:
Get-Content database\init.sql | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p123456
```

O usando MySQL Workbench:
1. Abre MySQL Workbench
2. Conecta con tu servidor local (localhost)
3. Abre el archivo `database/init.sql`
4. Ejecuta el script

### 3. Backend (Python Flask)

```bash
cd backend

# Crear entorno virtual
py -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# El archivo .env ya está configurado con:
# DB_NAME=tienda_online
# DB_USER=root
# DB_PASSWORD=123456

# Ejecutar servidor
py app.py
```

El backend estará disponible en: **http://localhost:5000**

### 4. Frontend (Angular 19)

Abre una nueva terminal:

```bash
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
│   ├── app.py              # Aplicación principal
│   ├── requirements.txt    # Dependencias Python
│   ├── .env               # Configuración (DB: tienda_online)
│   └── venv/              # Entorno virtual
├── database/              # Scripts de base de datos
│   ├── init.sql          # Script de inicialización
│   └── COMO_EJECUTAR.md  # Guía detallada
├── frontend/             # Frontend Angular 19
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   └── user-list/
│   │   │   ├── models/
│   │   │   │   └── user.model.ts
│   │   │   ├── services/
│   │   │   │   └── user.service.ts
│   │   │   └── app.component.ts
│   │   ├── index.html
│   │   └── main.ts
│   ├── angular.json
│   ├── package.json
│   └── node_modules/
└── README.md
```

## 🔌 API Endpoints

### Base URL: `http://localhost:5000`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Estado del servidor |
| GET | `/api/users` | Obtener todos los usuarios |
| GET | `/api/users/:id` | Obtener un usuario por ID |
| POST | `/api/users` | Crear un nuevo usuario |
| PUT | `/api/users/:id` | Actualizar un usuario |
| DELETE | `/api/users/:id` | Eliminar un usuario |

### Ejemplo de petición POST:
```json
{
  "name": "María González",
  "email": "maria@example.com"
}
```

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Angular 19** - Framework web moderno
- **TypeScript 5.6** - Lenguaje tipado
- **RxJS** - Programación reactiva
- **CSS3** - Estilos responsive

### Backend
- **Python 3.13** - Lenguaje de programación
- **Flask 3.0** - Micro-framework web
- **PyMySQL** - Conector MySQL puro Python
- **Flask-CORS** - Manejo de peticiones cross-origin
- **python-dotenv** - Variables de entorno

### Base de Datos
- **MySQL 8.0** - Sistema de gestión de base de datos relacional

## 💡 Características

✅ CRUD completo de usuarios  
✅ Interfaz moderna y responsive con gradientes  
✅ API RESTful con Flask  
✅ Validación de formularios  
✅ Manejo de errores robusto  
✅ Modal para crear/editar usuarios  
✅ Confirmación antes de eliminar  
✅ **Sin Docker** - instalación nativa  
✅ Base de datos MySQL `tienda_online`  

## 🔧 Comandos Útiles

### Backend
```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Ejecutar servidor
py app.py
```

### Frontend
```bash
# Compilar para producción
npm run build

# Ejecutar tests
npm test

# Generar nuevo componente
ng generate component nombre-componente

# Generar nuevo servicio
ng generate service nombre-servicio
```

### Base de Datos
```sql
-- Conectar a MySQL
USE tienda_online;

-- Ver usuarios
SELECT * FROM users;

-- Contar usuarios
SELECT COUNT(*) FROM users;

-- Limpiar tabla
TRUNCATE TABLE users;
```

## 🐛 Solución de Problemas

### Backend no inicia
- Verifica que el entorno virtual esté activado: `.\venv\Scripts\Activate.ps1`
- Verifica que MySQL esté corriendo
- Revisa las credenciales en `.env`

### Error de conexión a MySQL
- Verifica que MySQL Server esté ejecutándose
- Comprueba usuario y contraseña en `backend/.env`
- Verifica que la base de datos `tienda_online` exista

### Frontend no se conecta al backend
- Asegúrate de que el backend esté corriendo en el puerto 5000
- Verifica CORS en `app.py` (ya está configurado)
- Revisa la consola del navegador para errores

### Error al instalar dependencias Python en Windows
Si tienes problemas con `mysqlclient`, este proyecto usa `PyMySQL` que no requiere compilación.

## 📝 Configuración

### Variables de Entorno (backend/.env)
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=123456
DB_NAME=tienda_online
DB_PORT=3306
PORT=3000
JWT_SECRET=mi_clave_secreta_super_segura_123456
```

### Puerto del Frontend
Por defecto Angular corre en el puerto 4200. Para cambiarlo:
```bash
ng serve --port 4300
```

### Puerto del Backend
Por defecto Flask corre en el puerto 5000. Para cambiarlo, edita `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🚦 Estado del Proyecto

✅ Base de datos MySQL configurada con `tienda_online`  
✅ Backend Python Flask funcionando  
✅ Frontend Angular 19 listo  
✅ API RESTful completa  
✅ CRUD de usuarios implementado  
✅ Sin Docker - instalación nativa  

## 👥 Autor

**Leticia Orive**
- GitHub: [@Leticia-Orive](https://github.com/Leticia-Orive)

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 🎯 Próximos Pasos

Para expandir este proyecto puedes:
- Agregar gestión de productos
- Implementar carrito de compras
- Añadir autenticación con JWT
- Crear panel de administración
- Agregar categorías de productos
- Implementar sistema de pagos
- Añadir imágenes de productos
