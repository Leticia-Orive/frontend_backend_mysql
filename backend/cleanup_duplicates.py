import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def cleanup_duplicates():
    """Elimina las categorías de Mascotas duplicadas, dejando solo la primera"""
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
        
        # Obtener todas las categorías Mascotas principales
        cursor.execute("""
            SELECT id FROM categories 
            WHERE name = 'Mascotas' AND parent_id IS NULL 
            ORDER BY id
        """)
        mascotas_cats = cursor.fetchall()
        
        if len(mascotas_cats) > 1:
            keep_id = mascotas_cats[0]['id']
            print(f"Manteniendo categoría Mascotas con ID: {keep_id}")
            
            # Obtener IDs a eliminar
            delete_ids = [cat['id'] for cat in mascotas_cats[1:]]
            print(f"Eliminando categorías Mascotas con IDs: {delete_ids}")
            
            # Eliminar las categorías duplicadas (las subcategorías se eliminarán en cascada)
            for cat_id in delete_ids:
                cursor.execute("DELETE FROM categories WHERE id = %s", (cat_id,))
                print(f"  ✓ Eliminada categoría ID {cat_id}")
            
            connection.commit()
            print("\n✓ Limpieza completada!")
        else:
            print("No hay categorías Mascotas duplicadas.")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error al limpiar: {e}")

if __name__ == "__main__":
    cleanup_duplicates()
