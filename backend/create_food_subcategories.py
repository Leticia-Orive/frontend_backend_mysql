import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_food_subcategories():
    """Crea subcategorías para Alimentación con sus productos"""
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
        
        # Obtener el ID de la categoría Alimentación
        cursor.execute("SELECT id FROM categories WHERE name = 'Alimentación' AND parent_id IS NULL")
        alimentacion = cursor.fetchone()
        
        if not alimentacion:
            print("❌ No se encontró la categoría Alimentación")
            return
        
        alimentacion_id = alimentacion['id']
        print(f"✓ Categoría Alimentación encontrada (ID: {alimentacion_id})")
        
        # Eliminar productos directos de Alimentación
        cursor.execute("DELETE FROM products WHERE category_id = %s", (alimentacion_id,))
        print(f"✓ Eliminados productos directos de Alimentación")
        
        # Crear subcategorías
        print("\n=== CREANDO SUBCATEGORÍAS ===")
        subcategories = [
            ('Refrescos', 'Bebidas refrescantes y gaseosas', 'https://images.unsplash.com/photo-1581636625402-29b2a704ef13?w=400'),
            ('Infusiones', 'Tés e infusiones naturales', 'https://images.unsplash.com/photo-1597318114090-67f48a366184?w=400'),
            ('Cafés', 'Café en grano, molido y cápsulas', 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400'),
            ('Vinos', 'Vinos tintos, blancos y rosados', 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400'),
            ('Champán y Cava', 'Espumosos y cavas premium', 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=400'),
            ('Cervezas', 'Cervezas nacionales e importadas', 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400'),
            ('Alcohol', 'Licores, ron, whisky y más', 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400')
        ]
        
        subcat_ids = {}
        for name, desc, img in subcategories:
            cursor.execute("""
                INSERT INTO categories (name, description, image_url, parent_id) 
                VALUES (%s, %s, %s, %s)
            """, (name, desc, img, alimentacion_id))
            subcat_ids[name] = cursor.lastrowid
            print(f"  ✓ {name} (ID: {cursor.lastrowid})")
        
        connection.commit()
        
        # Insertar productos para cada subcategoría
        print("\n=== INSERTANDO PRODUCTOS ===")
        
        # Refrescos
        print("\nRefrescos:")
        refrescos_products = [
            ('Coca-Cola Original', 'Pack de 6 latas de 330ml', 4.99, 100, 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400'),
            ('Fanta Naranja', 'Pack de 6 latas de 330ml', 4.50, 80, 'https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=400'),
            ('Sprite Lima-Limón', 'Pack de 6 latas de 330ml', 4.50, 75, 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400'),
            ('Agua Mineral con Gas', 'Pack de 6 botellas de 500ml', 3.99, 120, 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400'),
            ('Zumo de Naranja Natural', 'Botella de 1 litro', 3.50, 60, 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400'),
            ('Nestea Limón', 'Pack de 6 botellas de 500ml', 5.99, 50, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400')
        ]
        for name, desc, price, stock, img in refrescos_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Refrescos']))
            print(f"  ✓ {name}")
        
        # Infusiones
        print("\nInfusiones:")
        infusiones_products = [
            ('Té Verde Sencha', 'Caja de 20 bolsitas', 3.99, 45, 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400'),
            ('Té Negro Earl Grey', 'Caja de 25 bolsitas', 4.50, 40, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400'),
            ('Manzanilla Natural', 'Caja de 20 bolsitas', 2.99, 60, 'https://images.unsplash.com/photo-1597318114090-67f48a366184?w=400'),
            ('Infusión de Jengibre y Limón', 'Caja de 20 bolsitas', 4.20, 35, 'https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?w=400'),
            ('Rooibos Vainilla', 'Caja de 20 bolsitas', 4.99, 30, 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400'),
            ('Té Chai Especiado', 'Caja de 20 bolsitas', 5.50, 25, 'https://images.unsplash.com/photo-1597318112693-23a0817d9a99?w=400')
        ]
        for name, desc, price, stock, img in infusiones_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Infusiones']))
            print(f"  ✓ {name}")
        
        # Cafés
        print("\nCafés:")
        cafes_products = [
            ('Café en Grano Arábica', 'Paquete de 1kg', 12.99, 40, 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400'),
            ('Café Molido Natural', 'Paquete de 250g', 4.99, 55, 'https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400'),
            ('Cápsulas Nespresso Intenso', 'Pack de 50 cápsulas', 15.99, 70, 'https://images.unsplash.com/photo-1610889556528-9a770e32642f?w=400'),
            ('Café Descafeinado', 'Paquete de 250g', 5.50, 45, 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400'),
            ('Café Expreso Premium', 'Paquete de 500g', 9.99, 35, 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400'),
            ('Café Soluble Instantáneo', 'Bote de 200g', 6.99, 50, 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400')
        ]
        for name, desc, price, stock, img in cafes_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Cafés']))
            print(f"  ✓ {name}")
        
        # Vinos
        print("\nVinos:")
        vinos_products = [
            ('Vino Tinto Rioja Crianza', 'Botella de 750ml', 8.99, 30, 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400'),
            ('Vino Blanco Albariño', 'Botella de 750ml', 9.50, 25, 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=400'),
            ('Vino Rosado Navarra', 'Botella de 750ml', 7.99, 35, 'https://images.unsplash.com/photo-1529686377437-8507f93d7a77?w=400'),
            ('Vino Tinto Reserva', 'Botella de 750ml', 15.99, 20, 'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=400'),
            ('Vino Blanco Verdejo', 'Botella de 750ml', 6.99, 40, 'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=400'),
            ('Vino Espumoso Prosecco', 'Botella de 750ml', 11.99, 28, 'https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?w=400')
        ]
        for name, desc, price, stock, img in vinos_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Vinos']))
            print(f"  ✓ {name}")
        
        # Champán y Cava
        print("\nChampán y Cava:")
        champan_products = [
            ('Cava Brut Nature', 'Botella de 750ml', 8.50, 25, 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=400'),
            ('Champagne Moët & Chandon', 'Botella de 750ml', 45.00, 10, 'https://images.unsplash.com/photo-1516594915697-87eb3b1c14ea?w=400'),
            ('Cava Rosado Semi Seco', 'Botella de 750ml', 9.99, 20, 'https://images.unsplash.com/photo-1510427079383-fc7adf933bae?w=400'),
            ('Cava Gran Reserva', 'Botella de 750ml', 16.99, 15, 'https://images.unsplash.com/photo-1557682224-5b8590cd9ec5?w=400'),
            ('Champagne Veuve Clicquot', 'Botella de 750ml', 55.00, 8, 'https://images.unsplash.com/photo-1599299327372-88c2f0c6c6b1?w=400'),
            ('Cava Brut Reserva', 'Botella de 750ml', 12.50, 18, 'https://images.unsplash.com/photo-1560148923-259d2c2d5f70?w=400')
        ]
        for name, desc, price, stock, img in champan_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Champán y Cava']))
            print(f"  ✓ {name}")
        
        # Cervezas
        print("\nCervezas:")
        cervezas_products = [
            ('Cerveza Estrella Galicia', 'Pack de 6 botellas de 330ml', 5.99, 80, 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400'),
            ('Cerveza Heineken', 'Pack de 6 latas de 330ml', 6.50, 70, 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400'),
            ('Cerveza Artesanal IPA', 'Pack de 4 botellas de 330ml', 8.99, 40, 'https://images.unsplash.com/photo-1532634993-15f421e42ec0?w=400'),
            ('Cerveza Sin Alcohol', 'Pack de 6 latas de 330ml', 4.99, 50, 'https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=400'),
            ('Cerveza Corona Extra', 'Pack de 6 botellas de 355ml', 7.99, 60, 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=400'),
            ('Cerveza Guinness', 'Pack de 4 latas de 440ml', 9.50, 35, 'https://images.unsplash.com/photo-1608849870759-be658f0f6d47?w=400')
        ]
        for name, desc, price, stock, img in cervezas_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Cervezas']))
            print(f"  ✓ {name}")
        
        # Alcohol
        print("\nAlcohol:")
        alcohol_products = [
            ('Ron Barceló Imperial', 'Botella de 700ml', 22.99, 25, 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400'),
            ('Whisky Johnnie Walker Red Label', 'Botella de 700ml', 18.99, 30, 'https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=400'),
            ('Vodka Absolut', 'Botella de 700ml', 16.50, 35, 'https://images.unsplash.com/photo-1560508880-e9e1ae57f6fd?w=400'),
            ('Ginebra Tanqueray', 'Botella de 700ml', 19.99, 28, 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=400'),
            ('Tequila José Cuervo', 'Botella de 700ml', 21.50, 20, 'https://images.unsplash.com/photo-1615332570393-2e4e4b9a1f19?w=400'),
            ('Licor Baileys', 'Botella de 700ml', 14.99, 40, 'https://images.unsplash.com/photo-1596285988045-59c7e08f2a17?w=400')
        ]
        for name, desc, price, stock, img in alcohol_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Alcohol']))
            print(f"  ✓ {name}")
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ ¡Subcategorías de Alimentación creadas exitosamente!")
        print("="*60)
        print(f"\nTotal de subcategorías creadas: {len(subcategories)}")
        print(f"Total de productos insertados: {len(refrescos_products) + len(infusiones_products) + len(cafes_products) + len(vinos_products) + len(champan_products) + len(cervezas_products) + len(alcohol_products)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_food_subcategories()
