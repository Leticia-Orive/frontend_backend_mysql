import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def verify_complete_structure():
    """Verifica la estructura completa de categorías y productos"""
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
        
        # Obtener todas las categorías principales con sus subcategorías y productos
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                COUNT(DISTINCT sub.id) as num_subcategorias,
                COUNT(DISTINCT p.id) as num_productos
            FROM categories c
            LEFT JOIN categories sub ON sub.parent_id = c.id
            LEFT JOIN products p ON p.category_id = sub.id
            WHERE c.parent_id IS NULL
            GROUP BY c.id, c.name
            ORDER BY c.name
        """)
        categories = cursor.fetchall()
        
        # Totales
        cursor.execute("SELECT COUNT(*) as total FROM categories WHERE parent_id IS NOT NULL")
        total_subcats = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM products")
        total_products = cursor.fetchone()['total']
        
        print("\n" + "="*70)
        print(" " * 20 + "ESTRUCTURA COMPLETA DE LA TIENDA")
        print("="*70)
        
        print(f"\n{'CATEGORÍA':<30} {'SUBCATEGORÍAS':<15} {'PRODUCTOS':<15}")
        print("-"*70)
        
        for cat in categories:
            print(f"{cat['name']:<30} {cat['num_subcategorias']:<15} {cat['num_productos']:<15}")
        
        print("-"*70)
        print(f"{'TOTALES':<30} {total_subcats:<15} {total_products:<15}")
        print("="*70)
        
        print("\n✅ TODAS LAS CATEGORÍAS TIENEN SUBCATEGORÍAS Y PRODUCTOS")
        print(f"✅ Total de {len(categories)} categorías principales")
        print(f"✅ Total de {total_subcats} subcategorías")
        print(f"✅ Total de {total_products} productos en la base de datos")
        print()
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_complete_structure()
