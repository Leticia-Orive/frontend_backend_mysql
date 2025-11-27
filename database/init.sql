-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS tiendas_online;
USE tiendas_online;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Limpiar tabla si ya existe datos
TRUNCATE TABLE users;

-- Insertar datos de ejemplo (password: 123456)
-- Primer usuario es admin, el resto son usuarios normales
INSERT INTO users (name, email, password, role) VALUES
('Admin Usuario', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW7xqwZbWv4W', 'admin'),
('Juan Pérez', 'juan.perez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW7xqwZbWv4W', 'user'),
('María García', 'maria.garcia@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW7xqwZbWv4W', 'user'),
('Carlos López', 'carlos.lopez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW7xqwZbWv4W', 'user'),
('Ana Martínez', 'ana.martinez@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lW7xqwZbWv4W', 'user');

-- Crear tabla de categorías
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(255),
    parent_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_category_name (name, parent_id)
);

-- Crear tabla de productos
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    image_url VARCHAR(255),
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Insertar categorías principales
INSERT INTO categories (name, description, image_url, parent_id) VALUES
('Electrónica', 'Dispositivos electrónicos y gadgets', 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400', NULL),
('Ropa', 'Ropa y accesorios de moda', 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400', NULL),
('Hogar', 'Artículos para el hogar y decoración', 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400', NULL),
('Deportes', 'Equipamiento deportivo y fitness', 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400', NULL),
('Libros', 'Libros y material educativo', 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400', NULL),
('Juguetes', 'Juguetes y entretenimiento infantil', 'https://images.unsplash.com/photo-1560582861-45078880e48e?w=400', NULL),
('Mascotas', 'Todo para tus mascotas', 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400', NULL);

-- Insertar subcategorías de Mascotas
INSERT INTO categories (name, description, image_url, parent_id) VALUES
('Complementos', 'Accesorios y complementos para mascotas', 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400', 7),
('Alimentación', 'Comida y snacks para mascotas', 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400', 7),
('Animales', 'Mascotas en venta', 'https://images.unsplash.com/photo-1415369629372-26f2fe60c467?w=400', 7);

-- Insertar productos de ejemplo
INSERT INTO products (name, description, price, stock, image_url, category_id) VALUES
-- Electrónica
('Laptop HP 15"', 'Laptop HP con procesador Intel Core i5, 8GB RAM, 256GB SSD', 899.99, 15, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400', 1),
('Smartphone Samsung Galaxy', 'Teléfono Samsung Galaxy con pantalla AMOLED 6.5"', 699.99, 25, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400', 1),
('Auriculares Bluetooth', 'Auriculares inalámbricos con cancelación de ruido', 149.99, 50, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', 1),
('Tablet 10"', 'Tablet Android con 64GB de almacenamiento', 299.99, 30, 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400', 1),

-- Ropa
('Camiseta Básica', 'Camiseta de algodón 100% en varios colores', 19.99, 100, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400', 2),
('Jeans Clásicos', 'Pantalones jeans de corte clásico', 49.99, 60, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400', 2),
('Chaqueta de Cuero', 'Chaqueta de cuero sintético estilo casual', 89.99, 20, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400', 2),
('Zapatillas Deportivas', 'Zapatillas cómodas para uso diario', 69.99, 45, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400', 2),

-- Hogar
('Lámpara de Mesa', 'Lámpara LED moderna para escritorio', 34.99, 40, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400', 3),
('Cojines Decorativos', 'Set de 4 cojines decorativos', 29.99, 55, 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400', 3),
('Espejo de Pared', 'Espejo decorativo con marco dorado', 79.99, 15, 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400', 3),
('Alfombra Moderna', 'Alfombra de 2x3 metros diseño moderno', 159.99, 10, 'https://images.unsplash.com/photo-1600166898405-da9535204843?w=400', 3),

-- Deportes
('Balón de Fútbol', 'Balón profesional tamaño 5', 24.99, 70, 'https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aac?w=400', 4),
('Mancuernas 5kg', 'Par de mancuernas de 5kg cada una', 39.99, 35, 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400', 4),
('Esterilla de Yoga', 'Esterilla antideslizante para yoga y pilates', 29.99, 50, 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400', 4),
('Bicicleta de Montaña', 'Bicicleta MTB 21 velocidades', 449.99, 8, 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=400', 4),

-- Libros
('El Quijote', 'Clásico de la literatura española', 15.99, 80, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400', 5),
('Programación Python', 'Guía completa de Python para principiantes', 39.99, 40, 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=400', 5),
('Cocina Mediterránea', 'Recetas tradicionales del Mediterráneo', 24.99, 30, 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400', 5),
('Historia del Arte', 'Compendio ilustrado de historia del arte', 49.99, 20, 'https://images.unsplash.com/photo-1513001900722-370f803f498d?w=400', 5),

-- Juguetes
('LEGO Ciudad', 'Set de construcción LEGO con 500 piezas', 59.99, 25, 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400', 6),
('Muñeca Interactiva', 'Muñeca que habla y canta', 44.99, 30, 'https://images.unsplash.com/photo-1572375992501-4b0892d50c69?w=400', 6),
('Rompecabezas 1000 piezas', 'Rompecabezas de paisaje natural', 19.99, 45, 'https://images.unsplash.com/photo-1586943759442-3f0b45f3f31e?w=400', 6),
('Coche Teledirigido', 'Coche RC con control remoto', 79.99, 18, 'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400', 6),

-- Mascotas - Complementos
('Collar para Perro', 'Collar ajustable de nylon resistente', 12.99, 50, 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400', 8),
('Correa Extensible', 'Correa retráctil de 5 metros', 24.99, 35, 'https://images.unsplash.com/photo-1583511655826-05700d3f5501?w=400', 8),
('Cama para Gato', 'Cama suave y cómoda para gatos', 34.99, 25, 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400', 8),
('Juguete Pelota', 'Pelota de goma para perros', 8.99, 80, 'https://images.unsplash.com/photo-1606214174585-fe31582dc6ee?w=400', 8),
('Transportín', 'Transportín para gatos y perros pequeños', 49.99, 20, 'https://images.unsplash.com/photo-1544306094-e2dcf9479da3?w=400', 8),
('Rascador para Gatos', 'Rascador de sisal con plataforma', 39.99, 30, 'https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400', 8),

-- Mascotas - Alimentación
('Pienso para Perros', 'Alimento seco premium para perros adultos 10kg', 45.99, 40, 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400', 9),
('Comida para Gatos', 'Alimento húmedo para gatos variedad pack 12 latas', 18.99, 60, 'https://images.unsplash.com/photo-1579158620246-c571a5f4e4e7?w=400', 9),
('Snacks Dentales', 'Premios dentales para perros', 9.99, 70, 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?w=400', 9),
('Golosinas para Gatos', 'Snacks crujientes para gatos sabor pollo', 6.99, 55, 'https://images.unsplash.com/photo-1516750342352-817451a4a07e?w=400', 9),
('Comida para Pájaros', 'Mezcla de semillas para pájaros 2kg', 14.99, 45, 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400', 9),
('Alimento para Peces', 'Escamas nutritivas para peces tropicales', 7.99, 65, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400', 9),

-- Mascotas - Animales
('Cachorro Golden Retriever', 'Cachorro golden retriever de 2 meses', 800.00, 2, 'https://images.unsplash.com/photo-1633722715463-d30f4f325e24?w=400', 10),
('Gatito Persa', 'Gatito persa de 3 meses', 600.00, 3, 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400', 10),
('Hámster Dorado', 'Hámster dorado adulto', 15.00, 10, 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400', 10),
('Canario Amarillo', 'Canario amarillo cantarín', 45.00, 8, 'https://images.unsplash.com/photo-1582142306909-195724d33d9e?w=400', 10),
('Pez Betta', 'Pez betta de colores variados', 12.00, 15, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400', 10),
('Conejo Enano', 'Conejo enano holandés', 75.00, 5, 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400', 10);
