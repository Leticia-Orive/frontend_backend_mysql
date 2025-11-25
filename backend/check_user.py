import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

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
        cur.execute("SELECT id, name, email, role FROM users WHERE email = 'le@gmail.com'")
        user = cur.fetchone()
        
        if user:
            print(f"✓ Usuario encontrado:")
            print(f"  ID: {user['id']}")
            print(f"  Nombre: {user['name']}")
            print(f"  Email: {user['email']}")
            print(f"  Rol: {user['role']}")
        else:
            print("✗ Usuario NO encontrado con email: le@gmail.com")
            print("\nUsuarios existentes:")
            cur.execute("SELECT id, name, email, role FROM users LIMIT 5")
            users = cur.fetchall()
            for u in users:
                print(f"  - {u['email']} ({u['role']})")
        
finally:
    conn.close()
