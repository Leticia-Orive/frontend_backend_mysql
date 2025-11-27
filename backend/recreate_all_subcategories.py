import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def recreate_all_subcategories():
    """Recrea todas las subcategorías y productos"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'tiendas_online'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Primero eliminar todas las subcategorías y productos existentes
        print("Limpiando datos existentes...")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM categories WHERE parent_id IS NOT NULL")
        connection.commit()
        print("✓ Datos limpiados\n")
        
        # Definir todas las categorías con sus subcategorías y productos
        all_categories = {
            'Electrónica': {
                'subcategories': [
                    ('Móviles y Tablets', 'Smartphones y tablets', 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'),
                    ('Ordenadores', 'Portátiles y equipos de sobremesa', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'),
                    ('Audio', 'Auriculares y altavoces', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'),
                    ('Fotografía', 'Cámaras y accesorios', 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400'),
                    ('Gaming', 'Consolas y videojuegos', 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400'),
                    ('Smartwatches', 'Relojes inteligentes', 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400')
                ],
                'products': {
                    'Móviles y Tablets': [
                        ('iPhone 14 Pro', 'Smartphone Apple 256GB', 1199.00, 15, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'),
                        ('Samsung Galaxy S23', 'Android 128GB', 899.00, 20, 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400'),
                        ('iPad Air', 'Tablet Apple 10.9"', 699.00, 12, 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400'),
                        ('Samsung Galaxy Tab', 'Tablet Android 11"', 449.00, 18, 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=400'),
                        ('Xiaomi Redmi Note', 'Smartphone 128GB', 299.00, 30, 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400'),
                        ('Funda Universal Tablet', 'Protección para tablets', 24.99, 50, 'https://images.unsplash.com/photo-1585792180666-f7347c490ee2?w=400')
                    ],
                    'Ordenadores': [
                        ('MacBook Pro 14"', 'Portátil Apple M2', 2299.00, 10, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400'),
                        ('Dell XPS 15', 'Portátil i7 16GB RAM', 1599.00, 12, 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400'),
                        ('PC Gaming Torre', 'i9, RTX 4070, 32GB RAM', 1899.00, 8, 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400'),
                        ('Monitor 27" 4K', 'Monitor IPS HDR', 399.00, 20, 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400'),
                        ('Teclado Mecánico RGB', 'Switches Cherry MX', 129.00, 35, 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=400'),
                        ('Ratón Gaming', 'DPI ajustable RGB', 69.99, 40, 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400')
                    ],
                    'Audio': [
                        ('AirPods Pro 2', 'Auriculares inalámbricos Apple', 279.00, 25, 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400'),
                        ('Sony WH-1000XM5', 'Auriculares con cancelación de ruido', 349.00, 18, 'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400'),
                        ('JBL Flip 6', 'Altavoz Bluetooth portátil', 119.00, 30, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400'),
                        ('Bose SoundLink', 'Altavoz premium', 199.00, 22, 'https://images.unsplash.com/photo-1545127398-14699f92334b?w=400'),
                        ('Auriculares Gaming', 'Sonido envolvente 7.1', 89.99, 35, 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400'),
                        ('Micrófono USB', 'Para streaming y podcasts', 79.99, 28, 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=400')
                    ],
                    'Fotografía': [
                        ('Canon EOS R6', 'Cámara mirrorless 20MP', 2499.00, 8, 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400'),
                        ('Sony Alpha A7 IV', 'Cámara full frame', 2599.00, 6, 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400'),
                        ('Objetivo Canon 24-70mm', 'Lente zoom f/2.8', 1299.00, 10, 'https://images.unsplash.com/photo-1606240474536-52e8db2ec2f6?w=400'),
                        ('Trípode Profesional', 'Aluminio ajustable', 89.99, 25, 'https://images.unsplash.com/photo-1606859580293-99cac60f5c37?w=400'),
                        ('Flash Externo', 'TTL para Canon/Nikon', 159.00, 15, 'https://images.unsplash.com/photo-1617395807183-fbc42dcc084e?w=400'),
                        ('Mochila Fotográfica', 'Capacidad para 2 cámaras', 79.99, 20, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400')
                    ],
                    'Gaming': [
                        ('PlayStation 5', 'Consola Sony 825GB', 549.00, 12, 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400'),
                        ('Xbox Series X', 'Consola Microsoft 1TB', 499.00, 10, 'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400'),
                        ('Nintendo Switch OLED', 'Consola híbrida', 349.00, 18, 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400'),
                        ('Mando DualSense', 'Controller PS5', 69.99, 30, 'https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=400'),
                        ('Silla Gaming', 'Ergonómica reclinable', 249.00, 15, 'https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=400'),
                        ('Volante Racing', 'Force feedback', 299.00, 12, 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=400')
                    ],
                    'Smartwatches': [
                        ('Apple Watch Series 9', 'Reloj inteligente Apple', 449.00, 20, 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400'),
                        ('Samsung Galaxy Watch 6', 'Smartwatch Android', 349.00, 25, 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400'),
                        ('Garmin Fenix 7', 'Reloj deportivo GPS', 599.00, 12, 'https://images.unsplash.com/photo-1557438159-51eec7a6c9e8?w=400'),
                        ('Fitbit Charge 5', 'Pulsera de actividad', 149.00, 30, 'https://images.unsplash.com/photo-1575403071235-f80f5eb99c11?w=400'),
                        ('Amazfit GTR 4', 'Smartwatch económico', 199.00, 28, 'https://images.unsplash.com/photo-1617043983671-adaadcaa2460?w=400'),
                        ('Correa Apple Watch', 'Silicona deportiva', 29.99, 50, 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400')
                    ]
                }
            },
            'Ropa': {
                'subcategories': [
                    ('Hombre', 'Moda masculina', 'https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=400'),
                    ('Mujer', 'Moda femenina', 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400'),
                    ('Niños', 'Ropa infantil', 'https://images.unsplash.com/photo-1503919005314-30d93d07d823?w=400'),
                    ('Calzado', 'Zapatos y zapatillas', 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400'),
                    ('Accesorios', 'Complementos de moda', 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400'),
                    ('Deportiva', 'Ropa deportiva', 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400')
                ],
                'products': {
                    'Hombre': [
                        ('Camisa Blanca Slim Fit', 'Algodón premium', 39.99, 40, 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400'),
                        ('Jeans Rectos Azules', 'Denim clásico', 59.99, 35, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'),
                        ('Chaqueta de Cuero', 'Piel sintética', 99.99, 20, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'),
                        ('Polo Lacoste', 'Algodón piqué', 79.99, 30, 'https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=400'),
                        ('Pantalón Chino', 'Corte recto beige', 49.99, 35, 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400'),
                        ('Sudadera con Capucha', 'Algodón felpa', 44.99, 45, 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400')
                    ],
                    'Mujer': [
                        ('Vestido Negro Elegante', 'Corte ajustado', 69.99, 25, 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400'),
                        ('Blusa Blanca Seda', 'Manga larga', 54.99, 30, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400'),
                        ('Jeans Skinny', 'Tiro alto azul oscuro', 49.99, 40, 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400'),
                        ('Abrigo de Lana', 'Color camel', 149.99, 15, 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=400'),
                        ('Falda Midi Plisada', 'Color negro', 39.99, 35, 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400'),
                        ('Camiseta Básica', 'Pack 3 unidades', 24.99, 60, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400')
                    ],
                    'Niños': [
                        ('Conjunto Deportivo Niño', 'Chandal 2 piezas', 34.99, 30, 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'),
                        ('Vestido Niña Flores', 'Algodón estampado', 29.99, 25, 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400'),
                        ('Vaqueros Niño', 'Denim elástico', 24.99, 35, 'https://images.unsplash.com/photo-1624378515195-6bbdb73dff1a?w=400'),
                        ('Sudadera con Capucha', 'Diseño infantil', 19.99, 45, 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400'),
                        ('Pijama 2 Piezas', 'Algodón suave', 16.99, 40, 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'),
                        ('Chaqueta Acolchada', 'Ligera e impermeable', 39.99, 28, 'https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=400')
                    ],
                    'Calzado': [
                        ('Zapatillas Nike Air Max', 'Running unisex', 129.99, 30, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'),
                        ('Botines Chelsea', 'Piel marrón', 89.99, 20, 'https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400'),
                        ('Sandalias de Verano', 'Mujer cómodas', 34.99, 40, 'https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400'),
                        ('Zapatos Oxford', 'Hombre vestir negro', 79.99, 25, 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=400'),
                        ('Bailarinas Planas', 'Varios colores', 29.99, 50, 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400'),
                        ('Botas de Agua', 'Impermeables', 39.99, 35, 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400')
                    ],
                    'Accesorios': [
                        ('Bolso de Mano Cuero', 'Color marrón', 79.99, 20, 'https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400'),
                        ('Cinturón de Piel', 'Hebilla plateada', 29.99, 40, 'https://images.unsplash.com/photo-1624222247344-550fb60583bb?w=400'),
                        ('Gafas de Sol Ray-Ban', 'Protección UV400', 149.99, 25, 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400'),
                        ('Bufanda de Lana', 'Colores variados', 24.99, 45, 'https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400'),
                        ('Cartera de Cuero', 'Hombre con cremallera', 34.99, 35, 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400'),
                        ('Gorro de Lana', 'Unisex invierno', 19.99, 50, 'https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=400')
                    ],
                    'Deportiva': [
                        ('Mallas de Running', 'Mujer transpirables', 39.99, 40, 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400'),
                        ('Camiseta Técnica Hombre', 'Dry-fit', 29.99, 50, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'),
                        ('Sujetador Deportivo', 'Alto impacto', 34.99, 35, 'https://images.unsplash.com/photo-1583675123553-f3b7e304187a?w=400'),
                        ('Pantalón Chándal', 'Algodón y poliéster', 44.99, 45, 'https://images.unsplash.com/photo-1584735175315-9d5df23860e6?w=400'),
                        ('Chaqueta Cortavientos', 'Impermeable ligera', 59.99, 30, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400'),
                        ('Calcetines Deportivos', 'Pack de 3 pares', 14.99, 60, 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400')
                    ]
                }
            },
            'Hogar': {
                'subcategories': [
                    ('Muebles', 'Muebles para el hogar', 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400'),
                    ('Decoración', 'Artículos decorativos', 'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=400'),
                    ('Textil', 'Textiles y telas', 'https://images.unsplash.com/photo-1631889993959-41b4e9c6e3c5?w=400'),
                    ('Cocina', 'Utensilios de cocina', 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400'),
                    ('Baño', 'Accesorios de baño', 'https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=400'),
                    ('Iluminación', 'Lámparas y luces', 'https://images.unsplash.com/photo-1543198126-a8ad8a2c9c1a?w=400')
                ],
                'products': {
                    'Muebles': [
                        ('Sofá 3 Plazas', 'Tapizado gris moderno', 599.00, 10, 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400'),
                        ('Mesa de Centro', 'Madera y cristal', 199.00, 15, 'https://images.unsplash.com/photo-1532372320572-cda25653a26d?w=400'),
                        ('Estantería Modular', '5 estantes blanca', 149.00, 20, 'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=400'),
                        ('Cama King Size', 'Estructura madera maciza', 699.00, 8, 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400'),
                        ('Sillón Relax', 'Reclinable beige', 399.00, 12, 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400'),
                        ('Escritorio Oficina', 'Con cajones 120cm', 249.00, 18, 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400')
                    ],
                    'Decoración': [
                        ('Cuadro Canvas Grande', 'Arte abstracto 90x60cm', 79.99, 25, 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=400'),
                        ('Jarrón Cerámico', 'Diseño minimalista', 34.99, 30, 'https://images.unsplash.com/photo-1578500494198-246f612d3b3d?w=400'),
                        ('Espejo Pared Redondo', 'Marco dorado 80cm', 89.99, 20, 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400'),
                        ('Set 3 Cojines Decorativos', 'Terciopelo colores', 44.99, 40, 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400'),
                        ('Alfombra Salon', '160x230cm moderna', 129.00, 15, 'https://images.unsplash.com/photo-1600166898405-da9535204843?w=400'),
                        ('Reloj Pared Moderno', 'Silencioso decorativo', 39.99, 35, 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400')
                    ],
                    'Textil': [
                        ('Juego Sábanas 150cm', 'Algodón 100%', 49.99, 30, 'https://images.unsplash.com/photo-1631889993959-41b4e9c6e3c5?w=400'),
                        ('Edredón Nórdico', 'Relleno 250gr', 79.99, 25, 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400'),
                        ('Cortinas Salón', 'Par 140x260cm', 59.99, 20, 'https://images.unsplash.com/photo-1585128903994-0f0c2b00f8e8?w=400'),
                        ('Toallas Baño Set 3', 'Algodón egipcio', 39.99, 40, 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=400'),
                        ('Manta Sofá', 'Suave 130x170cm', 29.99, 45, 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400'),
                        ('Funda Nórdica', 'Estampado moderno', 54.99, 28, 'https://images.unsplash.com/photo-1631889993959-41b4e9c6e3c5?w=400')
                    ],
                    'Cocina': [
                        ('Batidora Amasadora', '1000W con accesorios', 129.00, 20, 'https://images.unsplash.com/photo-1604335399105-a0c585fd81a1?w=400'),
                        ('Juego Sartenes', '3 piezas antiadherente', 89.99, 25, 'https://images.unsplash.com/photo-1584990347449-39b032b2e1cd?w=400'),
                        ('Robot de Cocina', 'Multifunción programable', 199.00, 15, 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=400'),
                        ('Cubertería 24 Piezas', 'Acero inoxidable', 49.99, 30, 'https://images.unsplash.com/photo-1600788907416-456578634209?w=400'),
                        ('Cafetera Express', '20 bares presión', 159.00, 18, 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400'),
                        ('Set Cuchillos', '6 piezas profesional', 79.99, 22, 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400')
                    ],
                    'Baño': [
                        ('Espejo con Luz LED', 'Antivaho 60x80cm', 149.00, 15, 'https://images.unsplash.com/photo-1620626011761-996317b8d101?w=400'),
                        ('Organizador Baño', 'Estante esquinero', 34.99, 30, 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400'),
                        ('Báscula Digital', 'Análisis corporal', 39.99, 35, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),
                        ('Dispensador Jabón', 'Automático sensor', 24.99, 40, 'https://images.unsplash.com/photo-1585421514738-01798e348b17?w=400'),
                        ('Alfombra Baño', 'Antideslizante memory', 19.99, 50, 'https://images.unsplash.com/photo-1620626011761-996317b8d101?w=400'),
                        ('Toallero Térmico', 'Eléctrico 8 barras', 89.99, 18, 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=400')
                    ],
                    'Iluminación': [
                        ('Lámpara Techo LED', 'Regulable moderna', 79.99, 25, 'https://images.unsplash.com/photo-1543198126-a8ad8a2c9c1a?w=400'),
                        ('Lámpara de Pie', 'Trípode madera', 89.99, 20, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400'),
                        ('Tira LED 5m', 'RGB con mando', 29.99, 45, 'https://images.unsplash.com/photo-1598982352866-fbe0ab4f4e7e?w=400'),
                        ('Plafón LED Cocina', '24W luz neutra', 34.99, 35, 'https://images.unsplash.com/photo-1550985543-49bee3167284?w=400'),
                        ('Lámpara Mesa Lectura', 'Flexible LED', 24.99, 40, 'https://images.unsplash.com/photo-1534105615256-13940a0e68d5?w=400'),
                        ('Foco Empotrable Pack 6', 'LED GU10', 44.99, 30, 'https://images.unsplash.com/photo-1550985543-49bee3167284?w=400')
                    ]
                }
            }
        }
        
        # Continuar con el resto de categorías...
        print("Creando subcategorías y productos...")
        print("="*60)
        
        total_subcats = 0
        total_products = 0
        
        for cat_name, cat_data in all_categories.items():
            cursor.execute("SELECT id FROM categories WHERE name = %s AND parent_id IS NULL", (cat_name,))
            category = cursor.fetchone()
            
            if not category:
                print(f"⚠️ Categoría {cat_name} no encontrada")
                continue
            
            cat_id = category['id']
            print(f"\n{cat_name} (ID: {cat_id})")
            
            # Crear subcategorías
            subcat_ids = {}
            for subcat_name, subcat_desc, subcat_img in cat_data['subcategories']:
                cursor.execute("""
                    INSERT INTO categories (name, description, image_url, parent_id) 
                    VALUES (%s, %s, %s, %s)
                """, (subcat_name, subcat_desc, subcat_img, cat_id))
                subcat_ids[subcat_name] = cursor.lastrowid
                total_subcats += 1
            
            connection.commit()
            
            # Insertar productos
            for subcat_name, products in cat_data['products'].items():
                for prod_name, prod_desc, price, stock, img in products:
                    cursor.execute("""
                        INSERT INTO products (name, description, price, stock, image_url, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (prod_name, prod_desc, price, stock, img, subcat_ids[subcat_name]))
                    total_products += 1
                print(f"  ✓ {subcat_name}: {len(products)} productos")
            
            connection.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Primera parte completada")
        print(f"Subcategorías: {total_subcats} | Productos: {total_products}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_all_subcategories()
