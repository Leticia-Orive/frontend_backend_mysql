USE tiendas_online;

ALTER TABLE categories DROP INDEX name;

ALTER TABLE categories ADD COLUMN parent_id INT DEFAULT NULL AFTER image_url;

ALTER TABLE categories ADD FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE;

ALTER TABLE categories ADD UNIQUE KEY unique_category_name (name, parent_id);

INSERT INTO categories (name, description, image_url, parent_id) VALUES
('Mascotas', 'Todo para tus mascotas', 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=400', NULL);

SET @mascotas_id = LAST_INSERT_ID();

INSERT INTO categories (name, description, image_url, parent_id) VALUES
('Complementos', 'Accesorios y complementos para mascotas', 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400', @mascotas_id),
('Alimentación', 'Comida y snacks para mascotas', 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400', @mascotas_id),
('Animales', 'Mascotas en venta', 'https://images.unsplash.com/photo-1415369629372-26f2fe60c467?w=400', @mascotas_id);

SET @complementos_id = (SELECT id FROM categories WHERE name = 'Complementos' AND parent_id = @mascotas_id);
SET @alimentacion_id = (SELECT id FROM categories WHERE name = 'Alimentación' AND parent_id = @mascotas_id);
SET @animales_id = (SELECT id FROM categories WHERE name = 'Animales' AND parent_id = @mascotas_id);

INSERT INTO products (name, description, price, stock, image_url, category_id) VALUES
('Collar para Perro', 'Collar ajustable de nylon resistente', 12.99, 50, 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400', @complementos_id),
('Correa Extensible', 'Correa retráctil de 5 metros', 24.99, 35, 'https://images.unsplash.com/photo-1583511655826-05700d3f5501?w=400', @complementos_id),
('Cama para Gato', 'Cama suave y cómoda para gatos', 34.99, 25, 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400', @complementos_id),
('Juguete Pelota', 'Pelota de goma para perros', 8.99, 80, 'https://images.unsplash.com/photo-1606214174585-fe31582dc6ee?w=400', @complementos_id),
('Transportín', 'Transportín para gatos y perros pequeños', 49.99, 20, 'https://images.unsplash.com/photo-1544306094-e2dcf9479da3?w=400', @complementos_id),
('Rascador para Gatos', 'Rascador de sisal con plataforma', 39.99, 30, 'https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400', @complementos_id);

INSERT INTO products (name, description, price, stock, image_url, category_id) VALUES
('Pienso para Perros', 'Alimento seco premium para perros adultos 10kg', 45.99, 40, 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400', @alimentacion_id),
('Comida para Gatos', 'Alimento húmedo para gatos variedad pack 12 latas', 18.99, 60, 'https://images.unsplash.com/photo-1579158620246-c571a5f4e4e7?w=400', @alimentacion_id),
('Snacks Dentales', 'Premios dentales para perros', 9.99, 70, 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?w=400', @alimentacion_id),
('Golosinas para Gatos', 'Snacks crujientes para gatos sabor pollo', 6.99, 55, 'https://images.unsplash.com/photo-1516750342352-817451a4a07e?w=400', @alimentacion_id),
('Comida para Pájaros', 'Mezcla de semillas para pájaros 2kg', 14.99, 45, 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400', @alimentacion_id),
('Alimento para Peces', 'Escamas nutritivas para peces tropicales', 7.99, 65, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400', @alimentacion_id);

INSERT INTO products (name, description, price, stock, image_url, category_id) VALUES
('Cachorro Golden Retriever', 'Cachorro golden retriever de 2 meses', 800.00, 2, 'https://images.unsplash.com/photo-1633722715463-d30f4f325e24?w=400', @animales_id),
('Gatito Persa', 'Gatito persa de 3 meses', 600.00, 3, 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400', @animales_id),
('Hámster Dorado', 'Hámster dorado adulto', 15.00, 10, 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400', @animales_id),
('Canario Amarillo', 'Canario amarillo cantarín', 45.00, 8, 'https://images.unsplash.com/photo-1582142306909-195724d33d9e?w=400', @animales_id),
('Pez Betta', 'Pez betta de colores variados', 12.00, 15, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400', @animales_id),
('Conejo Enano', 'Conejo enano holandés', 75.00, 5, 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400', @animales_id);
