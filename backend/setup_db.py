import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MySQL
conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    port=int(os.getenv('DB_PORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cur:
        # Leer el archivo SQL
        with open('../database/init.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar cada sentencia SQL
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cur.execute(statement)
                    conn.commit()
                    print(f"✓ Ejecutado: {statement[:50]}...")
                except Exception as e:
                    print(f"✗ Error en: {statement[:50]}...")
                    print(f"  Error: {str(e)}")
        
        print("\n✓ Script ejecutado correctamente!")
        
finally:
    conn.close()
