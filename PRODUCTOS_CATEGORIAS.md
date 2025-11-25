# Tienda Online - Sistema de Productos y Categorías

## ✨ Nuevas Funcionalidades Implementadas

### 🛒 Catálogo de Productos
- **Página Home renovada** con productos organizados por categorías
- **6 Categorías principales**: Electrónica, Ropa, Hogar, Deportes, Libros, Juguetes
- **24 productos de ejemplo** distribuidos entre las categorías
- **Filtrado por categoría** con botones interactivos
- **Diseño responsive** que se adapta a móviles y tablets

### 📦 Base de Datos

#### Nuevas Tablas Creadas

**Tabla `categories`:**
```sql
- id (PRIMARY KEY)
- name (VARCHAR 100, UNIQUE)
- description (TEXT)
- image_url (VARCHAR 255)
- created_at, updated_at (TIMESTAMPS)
```

**Tabla `products`:**
```sql
- id (PRIMARY KEY)
- name (VARCHAR 200)
- description (TEXT)
- price (DECIMAL 10,2)
- stock (INT)
- image_url (VARCHAR 255)
- category_id (FOREIGN KEY -> categories)
- created_at, updated_at (TIMESTAMPS)
```

### 🔧 Backend (Flask)

#### Nuevos Endpoints

**Categorías:**
- `GET /api/categories` - Obtener todas las categorías
- `GET /api/categories/{id}` - Obtener una categoría específica
- `GET /api/categories/{id}/products` - Obtener productos de una categoría

**Productos:**
- `GET /api/products` - Obtener todos los productos
- `GET /api/products?category_id={id}` - Filtrar productos por categoría
- `GET /api/products/{id}` - Obtener un producto específico

### 🎨 Frontend (Angular)

#### Nuevos Archivos Creados

**Modelos:**
- `models/category.model.ts` - Interfaz de categorías
- `models/product.model.ts` - Interfaz de productos

**Servicios:**
- `services/category.service.ts` - Servicio HTTP para categorías
- `services/product.service.ts` - Servicio HTTP para productos

**Componente Home Renovado:**
- Grid responsive de productos
- Filtrado por categorías
- Tarjetas de producto con imagen, descripción, precio y stock
- Badges de estado (Agotado, Últimas unidades)
- Header con información de usuario y acceso rápido

### 🎯 Características de la Interfaz

1. **Header Sticky**
   - Nombre de usuario y rol
   - Botón de acceso a gestión de usuarios (solo admin)
   - Botón de cerrar sesión

2. **Filtro de Categorías**
   - Botón "Todas" para ver todos los productos
   - Botones individuales por categoría
   - Estilo activo para la categoría seleccionada

3. **Tarjetas de Producto**
   - Imagen del producto con efecto hover
   - Nombre y descripción truncados
   - Precio formateado en euros
   - Indicador de stock disponible
   - Badge visual si está agotado o quedan pocas unidades
   - Botón "Añadir al carrito" (deshabilitado si no hay stock)

4. **Sección por Categoría**
   - Header con imagen y descripción de la categoría
   - Grid de productos pertenecientes a esa categoría
   - Mensaje si no hay productos en la categoría

## 🚀 Cómo Usar

### 1. Configurar la Base de Datos

Las tablas ya han sido creadas automáticamente. Si necesitas recrearlas:

```bash
cd backend
py setup_db.py
```

### 2. Iniciar el Backend

```bash
cd backend
py app.py
```

El servidor estará disponible en: `http://localhost:5000`

### 3. Iniciar el Frontend

```bash
cd frontend
ng serve
```

La aplicación estará disponible en: `http://localhost:4200`

### 4. Acceder a la Aplicación

1. **Registrarse o iniciar sesión**
2. **Explorar el catálogo** en la página home
3. **Filtrar por categorías** usando los botones superiores
4. **Ver productos** organizados por categoría con toda su información

## 📊 Datos de Ejemplo

### Categorías (6)
- Electrónica (4 productos)
- Ropa (4 productos)
- Hogar (4 productos)
- Deportes (4 productos)
- Libros (4 productos)
- Juguetes (4 productos)

### Productos (24 total)
Cada categoría tiene 4 productos de ejemplo con:
- Nombres descriptivos
- Precios variados
- Stock diferente
- Imágenes de Unsplash
- Descripciones detalladas

## 🎨 Diseño y UX

- **Paleta de colores**: Gradiente morado (#667eea, #764ba2)
- **Tipografía**: Sistema nativo del navegador
- **Responsive**: Breakpoints en 768px
- **Animaciones**: Hover suave en tarjetas y botones
- **Imágenes**: De alta calidad desde Unsplash

## 🔐 Control de Acceso

- **Usuarios normales**: Pueden ver el catálogo completo
- **Administradores**: Además pueden acceder a la gestión de usuarios

## 🛠 Tecnologías Utilizadas

**Backend:**
- Flask 3.x
- PyMySQL
- Flask-CORS
- JWT para autenticación

**Frontend:**
- Angular 19
- TypeScript
- Standalone Components
- RxJS

**Base de Datos:**
- MySQL 8.x
- Relaciones con Foreign Keys
- Timestamps automáticos

## 📝 Próximas Mejoras Sugeridas

1. ✅ Carrito de compras funcional
2. ✅ Gestión de productos (CRUD) para administradores
3. ✅ Búsqueda de productos por nombre
4. ✅ Ordenamiento (precio, nombre, stock)
5. ✅ Vista detallada de producto individual
6. ✅ Sistema de reseñas y calificaciones
7. ✅ Historial de pedidos
8. ✅ Procesamiento de pagos

## 🎉 ¡Listo para Usar!

Tu tienda online está completamente configurada con:
- ✅ Base de datos poblada con productos
- ✅ Backend con endpoints REST
- ✅ Frontend con interfaz moderna
- ✅ Sistema de autenticación y roles
- ✅ Catálogo de productos navegable
