from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import bcrypt

# Definir el blueprint para los usuarios
users_bp = Blueprint('users', __name__)

# Configurar la conexión a MongoDB 
client = MongoClient('mongodb://localhost:27017/')
db = client.Taskify  # Nombre de la base de datos
users_collection = db.users  # Colección de usuarios 

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Recibe los datos del usuario desde el cuerpo del request (JSON)
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Verificar si el usuario ya existe
        if users_collection.find_one({"email": email}):
            return jsonify({"error": "El usuario ya existe"}), 400

        # Hashear la contraseña usando bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Crear el objeto del usuario
        new_user = {
            "name": name,
            "email": email,
            "password_hash": password_hash.decode('utf-8'),
            "created_at": datetime.utcnow(),
            "last_login": None
        }

        # Insertar el nuevo usuario en la colección
        users_collection.insert_one(new_user)

        return jsonify({"message": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route('/update_user', methods=['PUT'])
def update_user():
    try:
        # Recibe los datos del usuario desde el cuerpo del request (JSON)
        data = request.json
        email = data.get('email')  # Identificar usuario por email
        updated_fields = {}

        # Verificar si el usuario existe
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar solo los campos proporcionados
        if data.get('name'):
            updated_fields['name'] = data.get('name')
        if data.get('password'):
            password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            updated_fields['password_hash'] = password_hash.decode('utf-8')

        # Actualizar la información del usuario en la base de datos
        if updated_fields:
            users_collection.update_one({"email": email}, {"$set": updated_fields})
            return jsonify({"message": "Información del usuario actualizada exitosamente"}), 200
        else:
            return jsonify({"error": "No hay campos para actualizar"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        # Recibe el correo del usuario desde el cuerpo del request (JSON)
        data = request.json
        email = data.get('email')

        # Verificar si el usuario existe
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Eliminar el usuario
        users_collection.delete_one({"email": email})

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        # Recibir los datos del usuario desde el cuerpo del request (JSON)
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validación de campos vacíos
        if not email or not password:
            return jsonify({"error": "El correo y la contraseña son obligatorios"}), 400

        # Verificar si el usuario existe
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401

        # Verificar la contraseña
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Actualizar el campo 'last_login'
            users_collection.update_one({"email": email}, {"$set": {"last_login": datetime.utcnow()}})
            return jsonify({"message": "Inicio de sesión exitoso"}), 200
        else:
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/logout', methods=['POST'])
def logout():
    try:
        # Recibir los datos del usuario desde el cuerpo del request (JSON)
        data = request.json
        email = data.get('email')

        # Validación de campos vacíos
        if not email:
            return jsonify({"error": "El correo es obligatorio"}), 400

        # Verificar si el usuario existe
        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar el campo 'last_login' al momento del logout
        users_collection.update_one({"email": email}, {"$set": {"last_login": datetime.utcnow()}})

        return jsonify({"message": "Cierre de sesión exitoso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
