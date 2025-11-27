# Subcategorías de Mascotas - Resumen de Implementación

## Descripción
Se ha implementado un sistema de categorías jerárquicas que permite tener subcategorías. Específicamente, se creó la categoría **Mascotas** con tres subcategorías:

### Subcategorías de Mascotas:
1. **Complementos** - Accesorios y complementos para mascotas
2. **Alimentación** - Comida y snacks para mascotas
3. **Animales** - Mascotas en venta

---

## Cambios en la Base de Datos

### Tabla `categories`
Se modificó para soportar jerarquías:
- Se agregó la columna `parent_id` (INT, DEFAULT NULL)
- Se agregó una clave foránea que referencia a `categories(id)` con CASCADE
- Se modificó el índice único para permitir nombres repetidos en diferentes niveles: `UNIQUE KEY unique_category_name (name, parent_id)`

### Datos Insertados

#### Categoría Principal
- **Mascotas** (ID: 16)

#### Subcategorías
- **Complementos** (ID: 27) - Padre: Mascotas
- **Alimentación** (ID: 28) - Padre: Mascotas
- **Animales** (ID: 29) - Padre: Mascotas

#### Productos por Subcategoría

**Complementos (6 productos):**
- Collar para Perro - $12.99 (Stock: 50)
- Correa Extensible - $24.99 (Stock: 35)
- Cama para Gato - $34.99 (Stock: 25)
- Juguete Pelota - $8.99 (Stock: 80)
- Transportín - $49.99 (Stock: 20)
- Rascador para Gatos - $39.99 (Stock: 30)

**Alimentación (6 productos):**
- Pienso para Perros - $45.99 (Stock: 40)
- Comida para Gatos - $18.99 (Stock: 60)
- Snacks Dentales - $9.99 (Stock: 70)
- Golosinas para Gatos - $6.99 (Stock: 55)
- Comida para Pájaros - $14.99 (Stock: 45)
- Alimento para Peces - $7.99 (Stock: 65)

**Animales (6 productos):**
- Cachorro Golden Retriever - $800.00 (Stock: 2)
- Gatito Persa - $600.00 (Stock: 3)
- Hámster Dorado - $15.00 (Stock: 10)
- Canario Amarillo - $45.00 (Stock: 8)
- Pez Betta - $12.00 (Stock: 15)
- Conejo Enano - $75.00 (Stock: 5)

---

## Cambios en el Backend (Flask)

### Archivo: `backend/app.py`

#### Endpoint: `GET /api/categories`
**Modificado** para soportar el parámetro `include_subcategories`:
- Sin parámetro o `include_subcategories=false`: Retorna solo categorías principales
- Con `include_subcategories=true`: Retorna categorías principales con sus subcategorías en estructura jerárquica

**Ejemplo de respuesta con subcategorías:**
```json
[
  {
    "id": 16,
    "name": "Mascotas",
    "description": "Todo para tus mascotas",
    "image_url": "https://...",
    "parent_id": null,
    "subcategories": [
      {
        "id": 27,
        "name": "Complementos",
        "description": "Accesorios y complementos para mascotas",
        "image_url": "https://...",
        "parent_id": 16
      },
      ...
    ]
  }
]
```

#### Endpoint: `GET /api/categories/:id`
**Modificado** para incluir subcategorías por defecto:
- Parámetro `include_subcategories=true` (por defecto): Incluye las subcategorías
- Parámetro `include_subcategories=false`: No incluye subcategorías

#### Endpoint: `GET /api/categories/:id/subcategories` (NUEVO)
Retorna todas las subcategorías de una categoría específica.

**Ejemplo:**
```
GET /api/categories/16/subcategories
```
Retorna las tres subcategorías de Mascotas.

---

## Cambios en el Frontend (Angular)

### Archivo: `frontend/src/app/models/category.model.ts`
Se actualizó el modelo para incluir:
```typescript
export interface Category {
  id: number;
  name: string;
  description: string;
  image_url: string;
  parent_id?: number | null;      // NUEVO
  created_at?: string;
  updated_at?: string;
  subcategories?: Category[];     // NUEVO
}
```

### Archivo: `frontend/src/app/services/category.service.ts`
Se actualizaron los métodos existentes y se agregó uno nuevo:

```typescript
// Método actualizado
getCategories(includeSubcategories: boolean = false): Observable<Category[]>

// Método actualizado
getCategory(id: number, includeSubcategories: boolean = true): Observable<Category>

// Método nuevo
getSubcategories(categoryId: number): Observable<Category[]>
```

---

## Scripts de Utilidad Creados

### `backend/migrate_subcategories.py`
Ejecuta la migración de la base de datos para agregar soporte de subcategorías.

### `backend/insert_pet_data.py`
Inserta la categoría Mascotas con sus subcategorías y productos.

### `backend/verify_subcategories.py`
Verifica que las categorías, subcategorías y productos se hayan creado correctamente.

### `backend/cleanup_duplicates.py`
Limpia categorías duplicadas que pudieran haberse creado.

### `backend/test_endpoints.py`
Prueba todos los endpoints relacionados con categorías y subcategorías.

---

## Cómo Usar

### Para filtrar productos por subcategoría:
```
GET /api/products?category_id=27
```
Esto retornará todos los productos de la subcategoría "Complementos".

### Para obtener la categoría Mascotas con todas sus subcategorías:
```
GET /api/categories/16?include_subcategories=true
```

### Para obtener solo las subcategorías de Mascotas:
```
GET /api/categories/16/subcategories
```

---

## Próximos Pasos Recomendados

1. **Frontend**: Actualizar los componentes para mostrar las subcategorías
2. **Frontend**: Implementar navegación jerárquica de categorías
3. **Frontend**: Agregar filtros por subcategoría en las vistas de productos
4. **Backend**: Considerar agregar endpoints para crear/editar/eliminar subcategorías
5. **Testing**: Crear pruebas unitarias y de integración para las nuevas funcionalidades

---

## Estructura Final

```
Mascotas (Categoría Principal)
├── Complementos (Subcategoría)
│   ├── Collar para Perro
│   ├── Correa Extensible
│   ├── Cama para Gato
│   ├── Juguete Pelota
│   ├── Transportín
│   └── Rascador para Gatos
├── Alimentación (Subcategoría)
│   ├── Pienso para Perros
│   ├── Comida para Gatos
│   ├── Snacks Dentales
│   ├── Golosinas para Gatos
│   ├── Comida para Pájaros
│   └── Alimento para Peces
└── Animales (Subcategoría)
    ├── Cachorro Golden Retriever
    ├── Gatito Persa
    ├── Hámster Dorado
    ├── Canario Amarillo
    ├── Pez Betta
    └── Conejo Enano
```
