import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_sports_subcategories():
    """Crea subcategorías para Deportes con sus productos"""
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
        
        # Obtener el ID de la categoría Deportes
        cursor.execute("SELECT id FROM categories WHERE name = 'Deportes' AND parent_id IS NULL")
        deportes = cursor.fetchone()
        
        if not deportes:
            print("❌ No se encontró la categoría Deportes")
            return
        
        deportes_id = deportes['id']
        print(f"✓ Categoría Deportes encontrada (ID: {deportes_id})")
        
        # Eliminar productos directos de Deportes
        cursor.execute("DELETE FROM products WHERE category_id = %s", (deportes_id,))
        print(f"✓ Eliminados productos directos de Deportes")
        
        # Crear subcategorías
        print("\n=== CREANDO SUBCATEGORÍAS ===")
        subcategories = [
            ('Fútbol', 'Equipamiento y accesorios de fútbol', 'https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aac?w=400'),
            ('Baloncesto', 'Material para básquet', 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400'),
            ('Tenis', 'Raquetas y accesorios de tenis', 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=400'),
            ('Running', 'Equipamiento para correr', 'https://images.unsplash.com/photo-1483721310020-03333e577078?w=400'),
            ('Natación', 'Material de natación y piscina', 'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=400'),
            ('Gimnasio', 'Equipamiento de fitness y gym', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400'),
            ('Ciclismo', 'Bicicletas y accesorios', 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400'),
            ('Yoga y Pilates', 'Accesorios para yoga y pilates', 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400')
        ]
        
        subcat_ids = {}
        for name, desc, img in subcategories:
            cursor.execute("""
                INSERT INTO categories (name, description, image_url, parent_id) 
                VALUES (%s, %s, %s, %s)
            """, (name, desc, img, deportes_id))
            subcat_ids[name] = cursor.lastrowid
            print(f"  ✓ {name} (ID: {cursor.lastrowid})")
        
        connection.commit()
        
        # Insertar productos para cada subcategoría
        print("\n=== INSERTANDO PRODUCTOS ===")
        
        # Fútbol
        print("\nFútbol:")
        futbol_products = [
            ('Balón de Fútbol Nike', 'Balón oficial tamaño 5', 24.99, 50, 'https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aac?w=400'),
            ('Botas de Fútbol Adidas', 'Tacos para césped natural', 79.99, 30, 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400'),
            ('Guantes de Portero', 'Guantes profesionales con grip', 34.99, 25, 'https://images.unsplash.com/photo-1551958219-acbc608c6377?w=400'),
            ('Espinilleras Nike', 'Protección ligera y resistente', 15.99, 60, 'https://images.unsplash.com/photo-1560272564-c83b66b1ad12?w=400'),
            ('Camiseta de Entrenamiento', 'Tejido transpirable Dry-Fit', 29.99, 45, 'https://images.unsplash.com/photo-1624526267942-ab0ff8a3e972?w=400'),
            ('Red Portería Reglamentaria', 'Red profesional 7.32 x 2.44m', 89.99, 10, 'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400')
        ]
        for name, desc, price, stock, img in futbol_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Fútbol']))
            print(f"  ✓ {name}")
        
        # Baloncesto
        print("\nBaloncesto:")
        baloncesto_products = [
            ('Balón Spalding NBA', 'Balón oficial de la NBA', 49.99, 35, 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400'),
            ('Zapatillas Nike Air Jordan', 'Zapatillas de baloncesto premium', 159.99, 20, 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=400'),
            ('Canasta Ajustable', 'Aro con altura regulable', 199.99, 8, 'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=400'),
            ('Camiseta NBA Oficial', 'Jersey oficial de equipo', 79.99, 25, 'https://images.unsplash.com/photo-1610116306796-6fea9f4fae38?w=400'),
            ('Muñequeras Deportivas', 'Par de muñequeras absorbentes', 9.99, 70, 'https://images.unsplash.com/photo-1515523110800-9415d13b84a8?w=400'),
            ('Bomba de Aire con Agujas', 'Inflador portátil', 12.99, 40, 'https://images.unsplash.com/photo-1515523110800-9415d13b84a8?w=400')
        ]
        for name, desc, price, stock, img in baloncesto_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Baloncesto']))
            print(f"  ✓ {name}")
        
        # Tenis
        print("\nTenis:")
        tenis_products = [
            ('Raqueta Wilson Pro Staff', 'Raqueta profesional', 189.99, 15, 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=400'),
            ('Pelotas de Tenis Wilson', 'Pack de 3 pelotas', 8.99, 80, 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=400'),
            ('Zapatillas Asics Gel Court', 'Zapatillas para pista dura', 89.99, 30, 'https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400'),
            ('Bolsa para Raquetas', 'Capacidad para 6 raquetas', 49.99, 20, 'https://images.unsplash.com/photo-1617883861744-5ce0d7ef5ec1?w=400'),
            ('Muñequera Head', 'Muñequera absorbente', 7.99, 60, 'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=400'),
            ('Cuerda para Raqueta', 'Set profesional de encordado', 24.99, 35, 'https://images.unsplash.com/photo-1617883861744-5ce0d7ef5ec1?w=400')
        ]
        for name, desc, price, stock, img in tenis_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Tenis']))
            print(f"  ✓ {name}")
        
        # Running
        print("\nRunning:")
        running_products = [
            ('Zapatillas Nike Air Zoom', 'Running para larga distancia', 129.99, 40, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'),
            ('Pulsómetro Garmin', 'Monitor de frecuencia cardíaca', 89.99, 25, 'https://images.unsplash.com/photo-1575403071235-f80f5eb99c11?w=400'),
            ('Mallas de Compresión', 'Mallas transpirables para running', 39.99, 50, 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400'),
            ('Riñonera Running', 'Porta objetos ligera e impermeable', 19.99, 45, 'https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400'),
            ('Gorra Deportiva', 'Gorra transpirable con protección UV', 14.99, 60, 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400'),
            ('Calcetines Running', 'Pack de 3 pares con tecnología anti-ampollas', 16.99, 70, 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400')
        ]
        for name, desc, price, stock, img in running_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Running']))
            print(f"  ✓ {name}")
        
        # Natación
        print("\nNatación:")
        natacion_products = [
            ('Gafas de Natación Speedo', 'Gafas profesionales anti-vaho', 24.99, 55, 'https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=400'),
            ('Bañador Arena Carbon', 'Bañador competición', 89.99, 30, 'https://images.unsplash.com/photo-1530549387789-4c1017266635?w=400'),
            ('Gorro de Silicona', 'Gorro ergonómico', 9.99, 80, 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400'),
            ('Aletas de Entrenamiento', 'Aletas cortas para técnica', 34.99, 35, 'https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=400'),
            ('Tabla de Natación', 'Tabla flotadora para ejercicios', 14.99, 45, 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=400'),
            ('Pull Buoy', 'Flotador para entrenamiento de brazos', 12.99, 40, 'https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=400')
        ]
        for name, desc, price, stock, img in natacion_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Natación']))
            print(f"  ✓ {name}")
        
        # Gimnasio
        print("\nGimnasio:")
        gimnasio_products = [
            ('Mancuernas Ajustables', 'Set de 2 mancuernas 2-24kg', 149.99, 20, 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400'),
            ('Banco de Musculación', 'Banco ajustable multiposición', 179.99, 15, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400'),
            ('Barra de Dominadas', 'Instalación en puerta sin tornillos', 34.99, 40, 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400'),
            ('Guantes de Gimnasio', 'Guantes con protección de muñeca', 19.99, 50, 'https://images.unsplash.com/photo-1584380931214-dbb5b72e93af?w=400'),
            ('Bandas Elásticas', 'Set de 5 bandas resistencia', 24.99, 60, 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400'),
            ('Rodillo de Espuma', 'Foam roller para masaje muscular', 29.99, 45, 'https://images.unsplash.com/photo-1599058917212-d750089bc07e?w=400')
        ]
        for name, desc, price, stock, img in gimnasio_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Gimnasio']))
            print(f"  ✓ {name}")
        
        # Ciclismo
        print("\nCiclismo:")
        ciclismo_products = [
            ('Bicicleta de Montaña', 'MTB aluminio 21 velocidades', 449.99, 12, 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=400'),
            ('Casco de Ciclismo', 'Casco aerodinámico con luz LED', 59.99, 35, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),
            ('Guantes de Ciclismo', 'Guantes con gel y dedos cortos', 24.99, 50, 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400'),
            ('Bomba de Piso', 'Inflador con manómetro', 29.99, 40, 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400'),
            ('Kit de Reparación', 'Herramientas y parches', 19.99, 55, 'https://images.unsplash.com/photo-1620249876429-9231c8e44ca7?w=400'),
            ('Maillot de Ciclismo', 'Camiseta técnica con bolsillos', 44.99, 30, 'https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=400')
        ]
        for name, desc, price, stock, img in ciclismo_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Ciclismo']))
            print(f"  ✓ {name}")
        
        # Yoga y Pilates
        print("\nYoga y Pilates:")
        yoga_products = [
            ('Esterilla de Yoga Premium', 'Grosor 6mm antideslizante', 34.99, 50, 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400'),
            ('Bloque de Yoga', 'Set de 2 bloques de corcho', 19.99, 45, 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400'),
            ('Correa de Yoga', 'Cinturón elástico 2.5m', 12.99, 60, 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400'),
            ('Pelota de Pilates', 'Balón fitness 65cm con bomba', 24.99, 35, 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400'),
            ('Rueda de Yoga', 'Aro para estiramientos y posturas', 39.99, 25, 'https://images.unsplash.com/photo-1599447332489-4d57c1f4ac7a?w=400'),
            ('Set Mancuernas Pilates', 'Par de pesas 1kg cada una', 16.99, 55, 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400')
        ]
        for name, desc, price, stock, img in yoga_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, desc, price, stock, img, subcat_ids['Yoga y Pilates']))
            print(f"  ✓ {name}")
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ ¡Subcategorías de Deportes creadas exitosamente!")
        print("="*60)
        print(f"\nTotal de subcategorías creadas: {len(subcategories)}")
        print(f"Total de productos insertados: {len(futbol_products) + len(baloncesto_products) + len(tenis_products) + len(running_products) + len(natacion_products) + len(gimnasio_products) + len(ciclismo_products) + len(yoga_products)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_sports_subcategories()
