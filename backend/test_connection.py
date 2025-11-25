"""
Script para probar la conexión a MySQL y diagnosticar problemas
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    print("Configuración de conexión:")
    print(f"  Host: {config['host']}")
    print(f"  User: {config['user']}")
    print(f"  Password: {'(vacía)' if not config['password'] else '***'}")
    print(f"  Port: {config['port']}")
    print()
    
    # Intentar conectar sin base de datos específica
    try:
        print("1. Intentando conectar a MySQL (sin base de datos)...")
        conn = pymysql.connect(**config)
        print("   ✅ Conexión exitosa!")
        
        # Listar bases de datos
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("\n2. Bases de datos disponibles:")
        for db in databases:
            print(f"   - {db[0]}")
        
        # Verificar si existe tiendas_online
        db_name = os.getenv('DB_NAME', 'tiendas_online')
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        if cursor.fetchone():
            print(f"\n3. ✅ La base de datos '{db_name}' existe")
            
            # Conectar a la base de datos y verificar tablas
            config['database'] = db_name
            conn2 = pymysql.connect(**config)
            cursor2 = conn2.cursor()
            cursor2.execute("SHOW TABLES")
            tables = cursor2.fetchall()
            print(f"\n4. Tablas en '{db_name}':")
            for table in tables:
                print(f"   - {table[0]}")
            cursor2.close()
            conn2.close()
        else:
            print(f"\n3. ❌ La base de datos '{db_name}' NO existe")
            print(f"\n   Para crearla, ejecuta:")
            print(f"   Get-Content database\\init.sql | & mysql -u {config['user']} -p")
        
        cursor.close()
        conn.close()
        
    except pymysql.err.OperationalError as e:
        print(f"   ❌ Error de conexión: {e}")
        print("\n🔧 Soluciones posibles:")
        print("   1. Verifica que MySQL esté corriendo:")
        print("      Get-Service MySQL80")
        print()
        print("   2. Si tu usuario root tiene contraseña, edita .env:")
        print("      DB_PASSWORD=tu_contraseña")
        print()
        print("   3. Si no tienes contraseña, configura una en MySQL:")
        print("      mysql -u root")
        print("      ALTER USER 'root'@'localhost' IDENTIFIED BY 'tu_nueva_contraseña';")
        print()
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_connection()
