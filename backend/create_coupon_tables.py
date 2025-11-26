import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MySQL
connection = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'tiendas_online'),
    port=int(os.getenv('DB_PORT', 3306))
)

try:
    with connection.cursor() as cursor:
        # Crear tabla de cupones de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_coupons (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                coupon_code VARCHAR(50) NOT NULL UNIQUE,
                discount_amount DECIMAL(10, 2) NOT NULL,
                is_used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_at TIMESTAMP NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_coupon_code (coupon_code),
                INDEX idx_is_used (is_used)
            )
        """)
        
        # Crear tabla de historial de compras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                discount_applied DECIMAL(10, 2) DEFAULT 0,
                coupon_used VARCHAR(50) NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user_id (user_id),
                INDEX idx_purchase_date (purchase_date)
            )
        """)
        
        connection.commit()
        print("✓ Tablas de cupones y compras creadas exitosamente")
        
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()
finally:
    connection.close()
