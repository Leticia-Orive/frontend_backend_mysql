import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MySQL
connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'tiendas_online'),
    port=int(os.getenv('DB_PORT', 3306))
)

try:
    with connection.cursor() as cursor:
        # Nuevas categorías
        new_categories = [
            ('Belleza y Cuidado Personal', 'Productos de belleza, maquillaje y cuidado', 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800'),
            ('Alimentación', 'Productos alimenticios y bebidas', 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=800'),
            ('Automóvil', 'Accesorios y productos para el coche', 'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800'),
            ('Mascotas', 'Productos para perros, gatos y mascotas', 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800'),
            ('Jardín', 'Herramientas y decoración para jardín', 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800'),
            ('Oficina', 'Material de oficina y papelería', 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800')
        ]
        
        cursor.executemany("""
            INSERT INTO categories (name, description, image_url)
            VALUES (%s, %s, %s)
        """, new_categories)
        
        print(f"✓ {len(new_categories)} nuevas categorías agregadas")
        
        # Obtener IDs de todas las categorías
        cursor.execute("SELECT id, name FROM categories ORDER BY id")
        categories = cursor.fetchall()
        
        # Crear diccionario con los nombres de categorías
        cursor.execute("SELECT id, name FROM categories ORDER BY id")
        category_dict = {}
        for row in cursor.fetchall():
            category_dict[row[1]] = row[0]  # name: id
        
        # Nuevos productos
        new_products = [
            # Belleza y Cuidado Personal (4 productos)
            ('Crema Facial Hidratante', 'Crema facial con ácido hialurónico y vitamina E', 24.99, 100, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500', category_dict.get('Belleza y Cuidado Personal')),
            ('Set de Maquillaje Profesional', 'Kit completo con paleta de sombras, labiales y pinceles', 49.99, 50, 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=500', category_dict.get('Belleza y Cuidado Personal')),
            ('Perfume Eau de Parfum', 'Fragancia floral con notas de jazmín y vainilla, 100ml', 69.99, 80, 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=500', category_dict.get('Belleza y Cuidado Personal')),
            ('Mascarilla Capilar Reparadora', 'Tratamiento intensivo para cabello dañado, 300ml', 18.99, 120, 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=500', category_dict.get('Belleza y Cuidado Personal')),
            
            # Alimentación (5 productos)
            ('Café Premium en Grano', 'Café 100% arábica de origen colombiano, 1kg', 15.99, 200, 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=500', category_dict.get('Alimentación')),
            ('Aceite de Oliva Extra Virgen', 'Aceite de primera presión en frío, 1L', 12.99, 150, 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500', category_dict.get('Alimentación')),
            ('Set de Especias Gourmet', 'Colección de 12 especias premium del mundo', 29.99, 80, 'https://images.unsplash.com/photo-1596040033229-a0b55c9abe3f?w=500', category_dict.get('Alimentación')),
            ('Chocolate Artesanal 80%', 'Tableta de chocolate negro premium, 200g', 8.99, 180, 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=500', category_dict.get('Alimentación')),
            ('Té Verde Orgánico', 'Caja de 50 bolsitas de té verde certificado', 9.99, 160, 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=500', category_dict.get('Alimentación')),
            
            # Automóvil (4 productos)
            ('Kit de Limpieza para Coche', 'Set completo con productos de limpieza profesional', 34.99, 70, 'https://images.unsplash.com/photo-1607860108855-64acf2078ed9?w=500', category_dict.get('Automóvil')),
            ('Soporte Universal para Móvil', 'Soporte magnético para smartphone con ventosa', 14.99, 250, 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=500', category_dict.get('Automóvil')),
            ('Cargador de Coche USB Doble', 'Cargador rápido 3.0A con doble puerto USB', 19.99, 180, 'https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=500', category_dict.get('Automóvil')),
            ('Organizador de Maletero', 'Organizador plegable con múltiples compartimentos', 24.99, 90, 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?w=500', category_dict.get('Automóvil')),
            
            # Mascotas (5 productos)
            ('Cama para Perro Grande', 'Cama ortopédica con colchón de memoria, 90x70cm', 54.99, 60, 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=500', category_dict.get('Mascotas')),
            ('Rascador para Gatos', 'Torre rascador de 120cm con plataformas y juguetes', 69.99, 45, 'https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=500', category_dict.get('Mascotas')),
            ('Comida Premium para Perros', 'Alimento natural sin cereales, 12kg', 44.99, 100, 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=500', category_dict.get('Mascotas')),
            ('Transportín de Viaje', 'Transportín homologado para avión, talla M', 39.99, 70, 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=500', category_dict.get('Mascotas')),
            ('Fuente de Agua Automática', 'Fuente con filtro y circulación continua, 2L', 32.99, 85, 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=500', category_dict.get('Mascotas')),
            
            # Jardín (4 productos)
            ('Set de Herramientas de Jardín', 'Kit de 6 herramientas con estuche', 39.99, 80, 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500', category_dict.get('Jardín')),
            ('Manguera Extensible 30m', 'Manguera flexible con pistola de riego 8 funciones', 29.99, 110, 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500', category_dict.get('Jardín')),
            ('Macetas Decorativas Set 3', 'Conjunto de macetas cerámicas con platillo', 34.99, 95, 'https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500', category_dict.get('Jardín')),
            ('Fertilizante Orgánico Universal', 'Abono natural para todo tipo de plantas, 5kg', 16.99, 140, 'https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=500', category_dict.get('Jardín')),
            
            # Oficina (5 productos)
            ('Agenda 2025 Premium', 'Agenda anual con planificador mensual y semanal', 19.99, 200, 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=500', category_dict.get('Oficina')),
            ('Set de Bolígrafos de Gel', 'Pack de 12 bolígrafos de colores variados', 12.99, 250, 'https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=500', category_dict.get('Oficina')),
            ('Archivador con 4 Cajones', 'Organizador de escritorio con múltiples compartimentos', 44.99, 60, 'https://images.unsplash.com/photo-1554838137-5c369fc1d1f8?w=500', category_dict.get('Oficina')),
            ('Lámpara LED de Escritorio', 'Lámpara ajustable con 3 niveles de brillo', 29.99, 120, 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=500', category_dict.get('Oficina')),
            ('Calculadora Científica', 'Calculadora programable con pantalla gráfica', 34.99, 90, 'https://images.unsplash.com/photo-1611696903-696162db8045?w=500', category_dict.get('Oficina')),
            
            # Más productos para categorías existentes
            # Electrónica
            ('Altavoz Bluetooth Portátil', 'Altavoz resistente al agua con 12h de batería', 39.99, 150, 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500', category_dict.get('Electrónica')),
            ('Webcam Full HD 1080p', 'Cámara web con micrófono integrado y enfoque automático', 54.99, 85, 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=500', category_dict.get('Electrónica')),
            ('Power Bank 20000mAh', 'Batería externa de carga rápida con 2 puertos USB', 34.99, 180, 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500', category_dict.get('Electrónica')),
            
            # Ropa
            ('Sudadera con Capucha Unisex', 'Sudadera de algodón orgánico en varios colores', 39.99, 200, 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500', category_dict.get('Ropa')),
            ('Zapatillas Deportivas Running', 'Zapatillas con amortiguación y tecnología transpirable', 79.99, 120, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500', category_dict.get('Ropa')),
            ('Mochila Urbana Impermeable', 'Mochila con compartimento para portátil 15.6"', 49.99, 95, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500', category_dict.get('Ropa')),
            
            # Hogar
            ('Robot Aspirador Inteligente', 'Aspirador con mapeo láser y app móvil', 199.99, 40, 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500', category_dict.get('Hogar')),
            ('Difusor de Aromas LED', 'Difusor ultrasónico con luz ambiental 7 colores', 29.99, 140, 'https://images.unsplash.com/photo-1602874801006-97f6dcbb4145?w=500', category_dict.get('Hogar')),
            ('Báscula Inteligente Digital', 'Báscula con análisis corporal y app Bluetooth', 39.99, 110, 'https://images.unsplash.com/photo-1582719471137-c3967ffb1c42?w=500', category_dict.get('Hogar')),
            
            # Deportes
            ('Esterilla de Yoga Premium', 'Esterilla antideslizante 180x60cm con bolsa', 34.99, 160, 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500', category_dict.get('Deportes')),
            ('Set de Pesas Ajustables', 'Mancuernas 2-24kg con soporte incluido', 149.99, 50, 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500', category_dict.get('Deportes')),
            ('Cuerda de Saltar Profesional', 'Comba con contador digital y peso ajustable', 19.99, 200, 'https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=500', category_dict.get('Deportes')),
            
            # Libros
            ('Colección Clásicos de la Literatura', 'Box set con 10 obras maestras de la literatura', 59.99, 70, 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500', category_dict.get('Libros')),
            ('Libro de Cocina Internacional', 'Recetas del mundo con fotos paso a paso', 29.99, 120, 'https://images.unsplash.com/photo-1606923829579-0cb981a83e2e?w=500', category_dict.get('Libros')),
            ('Novela Best Seller Thriller', 'Último thriller del autor más vendido', 18.99, 180, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500', category_dict.get('Libros')),
            
            # Juguetes
            ('LEGO Architecture Set', 'Set de construcción de edificio famoso, 2000 piezas', 89.99, 60, 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500', category_dict.get('Juguetes')),
            ('Dron con Cámara HD', 'Dron para principiantes con cámara 720p', 79.99, 45, 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=500', category_dict.get('Juguetes')),
            ('Puzzle 3D Torre Eiffel', 'Puzzle tridimensional con 816 piezas', 34.99, 85, 'https://images.unsplash.com/photo-1588421357574-87938a86fa28?w=500', category_dict.get('Juguetes'))
        ]
        
        # Filtrar productos que tengan category_id válido
        valid_products = [p for p in new_products if p[5] is not None]
        
        cursor.executemany("""
            INSERT INTO products (name, description, price, stock, image_url, category_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, valid_products)
        
        connection.commit()
        print(f"✓ {len(valid_products)} nuevos productos agregados")
        print("✓ Base de datos actualizada exitosamente")
        
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()
finally:
    connection.close()
