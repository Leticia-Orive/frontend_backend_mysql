import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MySQL
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'tiendas_online'),
    port=int(os.getenv('DB_PORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cur:
        # Verificar tablas existentes
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        print("Tablas en la base de datos:")
        for table in tables:
            print(f"  - {list(table.values())[0]}")
        
        print("\n" + "="*50)
        
        # Verificar categorías
        try:
            cur.execute("SELECT COUNT(*) as total FROM categories")
            result = cur.fetchone()
            print(f"\nCategorías: {result['total']} registros")
            
            cur.execute("SELECT id, name FROM categories")
            categories = cur.fetchall()
            for cat in categories:
                print(f"  - {cat['id']}: {cat['name']}")
        except Exception as e:
            print(f"\n✗ Error al consultar categories: {str(e)}")
        
        print("\n" + "="*50)
        
        # Verificar productos
        try:
            cur.execute("SELECT COUNT(*) as total FROM products")
            result = cur.fetchone()
            print(f"\nProductos: {result['total']} registros")
        except Exception as e:
            print(f"\n✗ Error al consultar products: {str(e)}")
        
finally:
    conn.close()
