import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def insert_pet_data():
    """Inserta las subcategorías y productos de Mascotas"""
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
        
        # Obtener el ID de la categoría Mascotas
        cursor.execute("SELECT id FROM categories WHERE name = 'Mascotas' AND parent_id IS NULL")
        mascotas = cursor.fetchone()
        
        if not mascotas:
            print("❌ No se encontró la categoría Mascotas")
            return
        
        mascotas_id = mascotas['id']
        print(f"✓ Categoría Mascotas encontrada (ID: {mascotas_id})")
        
        # Insertar subcategorías
        print("\nInsertando subcategorías...")
        subcategories = [
            ('Complementos', 'Accesorios y complementos para mascotas', 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400'),
            ('Alimentación', 'Comida y snacks para mascotas', 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400'),
            ('Animales', 'Mascotas en venta', 'https://images.unsplash.com/photo-1415369629372-26f2fe60c467?w=400')
        ]
        
        subcat_ids = {}
        for name, desc, img in subcategories:
            cursor.execute("""
                INSERT INTO categories (name, description, image_url, parent_id) 
                VALUES (%s, %s, %s, %s)
            """, (name, desc, img, mascotas_id))
            subcat_ids[name] = cursor.lastrowid
            print(f"  ✓ {name} (ID: {cursor.lastrowid})")
        
        connection.commit()
        
        # Insertar productos para Complementos
        print("\nInsertando productos de Complementos...")
        complementos_products = [
            ('Collar para Perro', 'Collar ajustable de nylon resistente', 12.99, 50, 'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400'),
            ('Correa Extensible', 'Correa retráctil de 5 metros', 24.99, 35, 'https://images.unsplash.com/photo-1583511655826-05700d3f5501?w=400'),
            ('Cama para Gato', 'Cama suave y cómoda para gatos', 34.99, 25, 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400'),
            ('Juguete Pelota', 'Pelota de goma para perros', 8.99, 80, 'https://images.unsplash.com/photo-1606214174585-fe31582dc6ee?w=400'),
            ('Transportín', 'Transportín para gatos y perros pequeños', 49.99, 20, 'https://images.unsplash.com/photo-1544306094-e2dcf9479da3?w=400'),
            ('Rascador para Gatos', 'Rascador de sisal con plataforma', 39.99, 30, 'https://images.unsplash.com/photo-1545249390-6bdfa286032f?w=400')
        ]
        
        for name, desc, price, stock, img in complementos_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Complementos']))
            print(f"  ✓ {name}")
        
        # Insertar productos para Alimentación
        print("\nInsertando productos de Alimentación...")
        alimentacion_products = [
            ('Pienso para Perros', 'Alimento seco premium para perros adultos 10kg', 45.99, 40, 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400'),
            ('Comida para Gatos', 'Alimento húmedo para gatos variedad pack 12 latas', 18.99, 60, 'https://images.unsplash.com/photo-1579158620246-c571a5f4e4e7?w=400'),
            ('Snacks Dentales', 'Premios dentales para perros', 9.99, 70, 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?w=400'),
            ('Golosinas para Gatos', 'Snacks crujientes para gatos sabor pollo', 6.99, 55, 'https://images.unsplash.com/photo-1516750342352-817451a4a07e?w=400'),
            ('Comida para Pájaros', 'Mezcla de semillas para pájaros 2kg', 14.99, 45, 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400'),
            ('Alimento para Peces', 'Escamas nutritivas para peces tropicales', 7.99, 65, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400')
        ]
        
        for name, desc, price, stock, img in alimentacion_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Alimentación']))
            print(f"  ✓ {name}")
        
        # Insertar productos para Animales
        print("\nInsertando productos de Animales...")
        animales_products = [
            ('Cachorro Golden Retriever', 'Cachorro golden retriever de 2 meses', 800.00, 2, 'https://images.unsplash.com/photo-1633722715463-d30f4f325e24?w=400'),
            ('Gatito Persa', 'Gatito persa de 3 meses', 600.00, 3, 'https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400'),
            ('Hámster Dorado', 'Hámster dorado adulto', 15.00, 10, 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?w=400'),
            ('Canario Amarillo', 'Canario amarillo cantarín', 45.00, 8, 'https://images.unsplash.com/photo-1582142306909-195724d33d9e?w=400'),
            ('Pez Betta', 'Pez betta de colores variados', 12.00, 15, 'https://images.unsplash.com/photo-1520990269481-36c4c03da56b?w=400'),
            ('Conejo Enano', 'Conejo enano holandés', 75.00, 5, 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400')
        ]
        
        for name, desc, price, stock, img in animales_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Animales']))
            print(f"  ✓ {name}")
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        print("\n✅ ¡Todos los datos de Mascotas se insertaron correctamente!")
        
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")

if __name__ == "__main__":
    insert_pet_data()
