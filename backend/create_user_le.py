import pymysql
import bcrypt
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
        # Verificar si el usuario ya existe
        cur.execute("SELECT id FROM users WHERE email = 'le@gmail.com'")
        existing_user = cur.fetchone()
        
        if existing_user:
            print("✓ El usuario le@gmail.com ya existe")
        else:
            # Crear el usuario con la contraseña que intentaste
            password = "123456"  # Puedes cambiar esta contraseña
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cur.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                ("Leticia", "le@gmail.com", hashed_password.decode('utf-8'), "admin")
            )
            conn.commit()
            print(f"✓ Usuario creado exitosamente:")
            print(f"  Email: le@gmail.com")
            print(f"  Contraseña: {password}")
            print(f"  Rol: admin")
        
finally:
    conn.close()
