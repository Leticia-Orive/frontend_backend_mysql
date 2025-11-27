import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def remove_products_from_main_category():
    """Elimina productos que están directamente en la categoría Mascotas (no en subcategorías)"""
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
        
        # Verificar si hay productos directamente en Mascotas
        cursor.execute("""
            SELECT id, name, price 
            FROM products 
            WHERE category_id = %s
        """, (mascotas_id,))
        products = cursor.fetchall()
        
        if len(products) == 0:
            print("\n✓ No hay productos directamente en la categoría Mascotas")
            print("  Todos los productos están en las subcategorías")
        else:
            print(f"\n⚠️  Se encontraron {len(products)} productos en la categoría Mascotas:")
            for prod in products:
                print(f"  - {prod['name']} (ID: {prod['id']}) - €{prod['price']}")
            
            # Eliminar los productos
            cursor.execute("DELETE FROM products WHERE category_id = %s", (mascotas_id,))
            connection.commit()
            print(f"\n✅ Se eliminaron {len(products)} productos de la categoría Mascotas")
        
        # Mostrar resumen de productos en subcategorías
        print("\n=== PRODUCTOS EN SUBCATEGORÍAS ===")
        cursor.execute("""
            SELECT c.name as subcategory, COUNT(p.id) as total
            FROM categories c
            LEFT JOIN products p ON p.category_id = c.id
            WHERE c.parent_id = %s
            GROUP BY c.id, c.name
            ORDER BY c.name
        """, (mascotas_id,))
        subcats = cursor.fetchall()
        
        for subcat in subcats:
            print(f"  • {subcat['subcategory']}: {subcat['total']} productos")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    remove_products_from_main_category()
