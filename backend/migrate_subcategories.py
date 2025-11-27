import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    """Ejecuta el script de migración para agregar subcategorías"""
    try:
        # Conectar a MySQL con la base de datos
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'tiendas_online'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        # Leer el archivo SQL de migración
        with open('../database/migrate_subcategories.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Dividir en comandos individuales
        commands = sql_content.split(';')
        
        print("Ejecutando migración para subcategorías de Mascotas...")
        print("-" * 60)
        
        success_count = 0
        error_count = 0
        
        for i, command in enumerate(commands, 1):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    connection.commit()
                    # Mostrar solo un resumen de cada comando
                    summary = command[:50].replace('\n', ' ')
                    print(f"✓ [{i}] Ejecutado: {summary}...")
                    success_count += 1
                except Exception as e:
                    summary = command[:50].replace('\n', ' ')
                    print(f"✗ [{i}] Error en: {summary}...")
                    print(f"  Error: {e}")
                    error_count += 1
                    # No detener la ejecución, continuar con el siguiente comando
        
        cursor.close()
        connection.close()
        
        print("-" * 60)
        print(f"Migración completada!")
        print(f"Comandos exitosos: {success_count}")
        print(f"Comandos con errores: {error_count}")
        
    except Exception as e:
        print(f"Error al ejecutar la migración: {e}")

if __name__ == "__main__":
    run_migration()
