from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import pymysql
import bcrypt
import jwt
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'mi_clave_secreta_super_segura_123456')

# Configuración de MySQL
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'tiendas_online'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

# Decorator para rutas protegidas
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Decorator para rutas que requieren rol de administrador
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            user_role = data.get('role', 'user')
            
            # Verificar que el usuario sea administrador
            if user_role != 'admin':
                return jsonify({'error': 'Acceso denegado. Se requiere rol de administrador'}), 403
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Ruta de bienvenida
@app.route('/')
def home():
    return jsonify({
        'message': 'API Tienda Online - Python Flask',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

# Registro de usuario
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Por defecto es 'user'
        
        if not name or not email or not password:
            return jsonify({'error': 'Nombre, email y contraseña son requeridos'}), 400
        
        # Validar rol
        if role not in ['admin', 'user']:
            return jsonify({'error': 'Rol inválido. Debe ser "admin" o "user"'}), 400
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si el email ya existe
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Insertar nuevo usuario con rol
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password.decode('utf-8'), role)
        )
        conn.commit()
        user_id = cur.lastrowid
        cur.close()
        conn.close()
        
        # Generar token
        token = jwt.encode({
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'token': token,
            'user': {
                'id': user_id,
                'name': name,
                'email': email,
                'role': role
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login de usuario
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Generar token con rol
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener perfil del usuario actual
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, role, created_at FROM users WHERE id = %s", (current_user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener todos los usuarios (solo administradores)
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users(current_user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, role, created_at FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener un usuario por ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Crear un nuevo usuario
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({'error': 'Nombre y email son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        user_id = cur.lastrowid
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'id': user_id,
            'name': name,
            'email': email
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Actualizar un usuario
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({'error': 'Nombre y email son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({
                'message': 'Usuario actualizado exitosamente',
                'id': user_id,
                'name': name,
                'email': email
            }), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Eliminar un usuario
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ ENDPOINTS DE CATEGORÍAS ============

# Obtener todas las categorías
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories ORDER BY name")
        categories = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener una categoría por ID
@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
        category = cur.fetchone()
        cur.close()
        conn.close()
        
        if category:
            return jsonify(category), 200
        return jsonify({'error': 'Categoría no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ ENDPOINTS DE PRODUCTOS ============

# Obtener todos los productos
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        category_id = request.args.get('category_id')
        conn = get_db_connection()
        cur = conn.cursor()
        
        if category_id:
            cur.execute("""
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                WHERE p.category_id = %s 
                ORDER BY p.name
            """, (category_id,))
        else:
            cur.execute("""
                SELECT p.*, c.name as category_name 
                FROM products p 
                JOIN categories c ON p.category_id = c.id 
                ORDER BY p.name
            """)
        
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener un producto por ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.id = %s
        """, (product_id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if product:
            return jsonify(product), 200
        return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener productos por categoría
@app.route('/api/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.category_id = %s 
            ORDER BY p.name
        """, (category_id,))
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Crear un nuevo producto (solo administradores)
@app.route('/api/products', methods=['POST'])
@admin_required
def create_product(current_user_id):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock', 0)
        image_url = data.get('image_url')
        category_id = data.get('category_id')
        
        if not name or not price or not category_id:
            return jsonify({'error': 'Nombre, precio y categoría son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products (name, description, price, stock, image_url, category_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, description, price, stock, image_url, category_id)
        )
        conn.commit()
        product_id = cur.lastrowid
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Producto creado exitosamente',
            'id': product_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Actualizar un producto (solo administradores)
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(current_user_id, product_id):
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        stock = data.get('stock')
        image_url = data.get('image_url')
        category_id = data.get('category_id')
        
        if not name or not price or not category_id:
            return jsonify({'error': 'Nombre, precio y categoría son requeridos'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE products SET name = %s, description = %s, price = %s, stock = %s, image_url = %s, category_id = %s WHERE id = %s",
            (name, description, price, stock, image_url, category_id, product_id)
        )
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Producto actualizado exitosamente'}), 200
        return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Eliminar un producto (solo administradores)
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(current_user_id, product_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== ENDPOINTS DE CUPONES ==========

# Obtener cupones del usuario actual
@app.route('/api/my-coupons', methods=['GET'])
@token_required
def get_my_coupons(current_user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Obtener cupones no usados
        cur.execute("""
            SELECT id, coupon_code, discount_amount, created_at
            FROM user_coupons
            WHERE user_id = %s AND is_used = FALSE
            ORDER BY created_at DESC
        """, (current_user_id,))
        
        coupons = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(coupons), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Usar un cupón
@app.route('/api/use-coupon', methods=['POST'])
@token_required
def use_coupon(current_user_id):
    try:
        data = request.get_json()
        coupon_code = data.get('coupon_code')
        
        if not coupon_code:
            return jsonify({'error': 'Código de cupón requerido'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar que el cupón existe, pertenece al usuario y no ha sido usado
        cur.execute("""
            SELECT id, discount_amount
            FROM user_coupons
            WHERE user_id = %s AND coupon_code = %s AND is_used = FALSE
        """, (current_user_id, coupon_code))
        
        coupon = cur.fetchone()
        
        if not coupon:
            cur.close()
            conn.close()
            return jsonify({'error': 'Cupón inválido o ya usado'}), 400
        
        # Marcar cupón como usado
        cur.execute("""
            UPDATE user_coupons
            SET is_used = TRUE, used_at = NOW()
            WHERE id = %s
        """, (coupon['id'],))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Cupón aplicado exitosamente',
            'discount_amount': float(coupon['discount_amount'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Generar cupón para el usuario (por cada compra)
def generate_coupon_code(user_id, purchase_count):
    """Genera un código de cupón único"""
    import random
    import string
    timestamp = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"USER{user_id}-{timestamp}-{random_str}"

# Procesar compra y generar cupón
@app.route('/api/checkout', methods=['POST'])
@token_required
def checkout(current_user_id):
    try:
        data = request.get_json()
        total_amount = data.get('total_amount')
        discount_applied = data.get('discount_applied', 0)
        coupon_used = data.get('coupon_used', None)
        
        if not total_amount:
            return jsonify({'error': 'Monto total requerido'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Registrar la compra
        cur.execute("""
            INSERT INTO purchase_history (user_id, total_amount, discount_applied, coupon_used)
            VALUES (%s, %s, %s, %s)
        """, (current_user_id, total_amount, discount_applied, coupon_used))
        
        purchase_id = cur.lastrowid
        
        # Contar cuántas compras ha hecho el usuario
        cur.execute("SELECT COUNT(*) as count FROM purchase_history WHERE user_id = %s", (current_user_id,))
        purchase_count = cur.fetchone()['count']
        
        # Generar cupón de descuento (por ejemplo, 5€ por cada compra)
        coupon_amount = 5.0
        coupon_code = generate_coupon_code(current_user_id, purchase_count)
        
        cur.execute("""
            INSERT INTO user_coupons (user_id, coupon_code, discount_amount)
            VALUES (%s, %s, %s)
        """, (current_user_id, coupon_code, coupon_amount))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Compra procesada exitosamente',
            'purchase_id': purchase_id,
            'new_coupon': {
                'code': coupon_code,
                'amount': coupon_amount
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
