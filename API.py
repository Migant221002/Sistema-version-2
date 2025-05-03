from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Configuración CORS
CORS(app, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:  # Si hay un origen en la petición
        response.headers['Access-Control-Allow-Origin'] = origin
    else:  # Si no hay origen, permitir localhost:3000
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization, X-Request-With'
    response.headers['Access-Control-Expose-Headers'] = '*'
    
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Max-Age'] = '1728000'
        response.headers['Content-Type'] = 'text/plain'
    
    return response

app.config['SECRET_KEY'] = os.urandom(24)

# Configuración de la base de datos
db_config = {
    'host': 'bglucmgbm4ndh8uojido-mysql.services.clever-cloud.com',
    'database': 'bglucmgbm4ndh8uojido',
    'user': 'u0mi0h3vk85jpjrk',
    'password': '2OMj4BJWJKwHLrC6HfEa',
    'port': '3306'
}

# Función para conectar a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Rutas de autenticación
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['username', 'password', 'email']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM usuarios WHERE username = %s", (data['username'],))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return jsonify({"message": "El usuario ya existe"}), 400
            
            # Crear nuevo usuario
            hashed_password = generate_password_hash(data['password'])
            query = "INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (data['username'], hashed_password, data['email']))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al registrar usuario"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (data['username'],))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user and check_password_hash(user['password'], data['password']):
                token = jwt.encode({
                    'user_id': user['id'],
                    'exp': datetime.utcnow() + timedelta(days=1)
                }, app.config['SECRET_KEY'])
                return jsonify({
                    "token": token,
                    "user": {
                        "id": user['id'],
                        "username": user['username']
                    }
                })
            return jsonify({"message": "Credenciales inválidas"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error en el login"}), 500

# Rutas de empleados
@app.route('/api/empleados', methods=['GET'])
def get_empleados():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM empleados")
            empleados = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(empleados)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([])

@app.route('/api/empleados', methods=['POST'])
def create_empleado():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['nombre', 'cedula', 'telefono']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO empleados (nombre, cedula, telefono) VALUES (%s, %s, %s)"
            cursor.execute(query, (data['nombre'], data['cedula'], data['telefono']))
            connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({"id": new_id, "message": "Empleado creado exitosamente"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al crear empleado"}), 500

@app.route('/api/empleados/<int:id>', methods=['PUT'])
def update_empleado(id):
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['nombre', 'cedula', 'telefono']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "UPDATE empleados SET nombre = %s, cedula = %s, telefono = %s WHERE id = %s"
            cursor.execute(query, (data['nombre'], data['cedula'], data['telefono'], id))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Empleado actualizado exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al actualizar empleado"}), 500

@app.route('/api/empleados/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM empleados WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Empleado eliminado exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al eliminar empleado"}), 500

# Rutas de fincas
@app.route('/api/fincas', methods=['GET'])
def get_fincas():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fincas")
            fincas = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(fincas)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([])

@app.route('/api/fincas', methods=['POST'])
def create_finca():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['nombre', 'ubicacion']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO fincas (nombre, ubicacion) VALUES (%s, %s)"
            cursor.execute(query, (data['nombre'], data['ubicacion']))
            connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({"id": new_id, "message": "Finca creada exitosamente"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al crear finca"}), 500

@app.route('/api/fincas/<int:id>', methods=['PUT'])
def update_finca(id):
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['nombre', 'ubicacion']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "UPDATE fincas SET nombre = %s, ubicacion = %s WHERE id = %s"
            cursor.execute(query, (data['nombre'], data['ubicacion'], id))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Finca actualizada exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al actualizar finca"}), 500

@app.route('/api/fincas/<int:id>', methods=['DELETE'])
def delete_finca(id):
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM fincas WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Finca eliminada exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al eliminar finca"}), 500

# Rutas de asignaciones
@app.route('/api/asignaciones', methods=['GET'])
def get_asignaciones():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    a.*,
                    e.nombre as empleado_nombre,
                    e.cedula as empleado_dpi,
                    e.telefono as empleado_telefono,
                    f.nombre as finca_nombre,
                    f.ubicacion as finca_ubicacion
                FROM asignaciones a 
                LEFT JOIN empleados e ON a.empleado_id = e.id 
                LEFT JOIN fincas f ON a.finca_id = f.id
            """)
            asignaciones = cursor.fetchall()
            cursor.close()
            connection.close()
            
            # Formatear los datos para el frontend
            formatted_asignaciones = []
            for asignacion in asignaciones:
                formatted_asignacion = {
                    "id": asignacion["id"],
                    "fecha_asignacion": asignacion["fecha_asignacion"],
                    "empleado": {
                        "id": asignacion["empleado_id"],
                        "nombre": asignacion["empleado_nombre"],
                        "dpi": asignacion["empleado_dpi"],
                        "telefono": asignacion["empleado_telefono"]
                    },
                    "finca": {
                        "id": asignacion["finca_id"],
                        "nombre": asignacion["finca_nombre"],
                        "ubicacion": asignacion["finca_ubicacion"]
                    }
                }
                formatted_asignaciones.append(formatted_asignacion)
            
            return jsonify(formatted_asignaciones)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([])

@app.route('/api/asignaciones', methods=['POST'])
def create_asignacion():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['empleado_id', 'finca_id']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO asignaciones (empleado_id, finca_id) VALUES (%s, %s)"
            cursor.execute(query, (data['empleado_id'], data['finca_id']))
            connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({"id": new_id, "message": "Asignación creada exitosamente"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al crear asignación"}), 500

@app.route('/api/asignaciones/<int:id>', methods=['PUT'])
def update_asignacion(id):
    try:
        data = request.get_json()
        print("Datos recibidos:", data)  # Debug
        
        if not data or not all(k in data for k in ['empleado_id', 'finca_id', 'fecha_asignacion']):
            return jsonify({"message": "Datos incompletos"}), 400
        
        # Convertir IDs a enteros
        empleado_id = int(data['empleado_id'])
        finca_id = int(data['finca_id'])
        fecha_asignacion = data['fecha_asignacion']
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            # Verificar si la asignación existe
            cursor.execute("SELECT id FROM asignaciones WHERE id = %s", (id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return jsonify({"message": "Asignación no encontrada"}), 404
            
            # Verificar si el empleado existe
            cursor.execute("SELECT id FROM empleados WHERE id = %s", (empleado_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return jsonify({"message": "Empleado no encontrado"}), 404
            
            # Verificar si la finca existe
            cursor.execute("SELECT id FROM fincas WHERE id = %s", (finca_id,))
            if not cursor.fetchone():
                cursor.close()
                connection.close()
                return jsonify({"message": "Finca no encontrada"}), 404
            
            # Actualizar la asignación
            query = """
                UPDATE asignaciones 
                SET empleado_id = %s, 
                    finca_id = %s, 
                    fecha_asignacion = %s 
                WHERE id = %s
            """
            cursor.execute(query, (empleado_id, finca_id, fecha_asignacion, id))
            connection.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                connection.close()
                return jsonify({
                    "message": "Asignación actualizada exitosamente",
                    "id": id,
                    "empleado_id": empleado_id,
                    "finca_id": finca_id,
                    "fecha_asignacion": fecha_asignacion
                }), 200
            else:
                cursor.close()
                connection.close()
                return jsonify({"message": "No se pudo actualizar la asignación"}), 500
    except ValueError as e:
        print("Error de conversión:", str(e))  # Debug
        return jsonify({"error": "Error en el formato de los datos"}), 400
    except Error as e:
        print("Error MySQL:", str(e))  # Debug
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print("Error general:", str(e))  # Debug
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/api/asignaciones/<int:id>', methods=['DELETE'])
def delete_asignacion(id):
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM asignaciones WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Asignación eliminada exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al eliminar asignación"}), 500

# Rutas de pagos
@app.route('/api/pagos', methods=['GET'])
def get_pagos():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    p.*,
                    e.nombre as empleado_nombre,
                    e.cedula as empleado_dpi,
                    e.telefono as empleado_telefono
                FROM pagos p 
                LEFT JOIN empleados e ON p.empleado_id = e.id
            """)
            pagos = cursor.fetchall()
            cursor.close()
            connection.close()
            
            # Formatear los datos para el frontend
            formatted_pagos = []
            for pago in pagos:
                formatted_pago = {
                    "id": pago["id"],
                    "fecha_pago": pago["fecha_pago"],
                    "libras": pago["libras"],
                    "precio_libra": pago["precio_libra"],
                    "total": pago["total"],
                    "empleado": {
                        "id": pago["empleado_id"],
                        "nombre": pago["empleado_nombre"],
                        "dpi": pago["empleado_dpi"],
                        "telefono": pago["empleado_telefono"]
                    }
                }
                formatted_pagos.append(formatted_pago)
            
            return jsonify(formatted_pagos)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify([])

@app.route('/api/pagos', methods=['POST'])
def create_pago():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['empleado_id', 'libras', 'precio_libra', 'fecha_pago']):  # ✅ Se asegura que fecha_pago esté presente
            return jsonify({"message": "Datos incompletos"}), 400
        
        total = float(data['libras']) * float(data['precio_libra'])
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "INSERT INTO pagos (empleado_id, libras, precio_libra, total, fecha_pago) VALUES (%s, %s, %s, %s, %s)"  # ✅ Se añade fecha_pago
            cursor.execute(query, (data['empleado_id'], data['libras'], data['precio_libra'], total, data['fecha_pago']))  # ✅ Se envía fecha_pago correctamente
            connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return jsonify({
                "id": new_id, 
                "message": "Pago registrado exitosamente",
                "total": total,
                "fecha_pago": data['fecha_pago']  # ✅ Se confirma la fecha guardada
            }), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al registrar pago"}), 500

@app.route('/api/pagos/<int:id>', methods=['PUT'])
def update_pago(id):
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['empleado_id', 'libras', 'precio_libra', 'fecha_pago']):  # ✅ Se verifica que fecha_pago esté presente
            return jsonify({"message": "Datos incompletos"}), 400
        
        total = float(data['libras']) * float(data['precio_libra'])
        
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "UPDATE pagos SET empleado_id = %s, libras = %s, precio_libra = %s, total = %s, fecha_pago = %s WHERE id = %s"  # ✅ Se incluye fecha_pago
            cursor.execute(query, (data['empleado_id'], data['libras'], data['precio_libra'], total, data['fecha_pago'], id))  # ✅ Se envía fecha_pago correctamente
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({
                "message": "Pago actualizado exitosamente",
                "fecha_pago": data['fecha_pago']  # ✅ Se confirma la fecha guardada
            }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al actualizar pago"}), 500

@app.route('/api/pagos/<int:id>', methods=['DELETE'])
def delete_pago(id):
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            query = "DELETE FROM pagos WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"message": "Pago eliminado exitosamente"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Error al eliminar pago"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)