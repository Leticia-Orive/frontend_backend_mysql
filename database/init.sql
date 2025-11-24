-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS tienda_online;
USE tienda_online;

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
