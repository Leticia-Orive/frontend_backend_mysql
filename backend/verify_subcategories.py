import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def verify_categories():
    """Verifica que las categorías y subcategorías se hayan creado correctamente"""
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
        
        print("\n=== CATEGORÍAS PRINCIPALES ===")
        cursor.execute("SELECT * FROM categories WHERE parent_id IS NULL ORDER BY name")
        main_categories = cursor.fetchall()
        for cat in main_categories:
            print(f"- {cat['name']} (ID: {cat['id']})")
        
        print("\n=== SUBCATEGORÍAS DE MASCOTAS ===")
        cursor.execute("""
            SELECT c.*, parent.name as parent_name 
            FROM categories c 
            JOIN categories parent ON c.parent_id = parent.id 
            WHERE parent.name = 'Mascotas'
            ORDER BY c.name
        """)
        subcategories = cursor.fetchall()
        for subcat in subcategories:
            print(f"- {subcat['name']} (ID: {subcat['id']}, Padre: {subcat['parent_name']})")
        
        print("\n=== PRODUCTOS POR SUBCATEGORÍA ===")
        for subcat in subcategories:
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM products 
                WHERE category_id = %s
            """, (subcat['id'],))
            result = cursor.fetchone()
            print(f"\n{subcat['name']}: {result['total']} productos")
            
            cursor.execute("""
                SELECT name, price, stock 
                FROM products 
                WHERE category_id = %s
                ORDER BY name
            """, (subcat['id'],))
            products = cursor.fetchall()
            for prod in products:
                print(f"  • {prod['name']} - ${prod['price']} (Stock: {prod['stock']})")
        
        cursor.close()
        connection.close()
        
        print("\n✓ Verificación completada!")
        
    except Exception as e:
        print(f"Error al verificar: {e}")

if __name__ == "__main__":
    verify_categories()
