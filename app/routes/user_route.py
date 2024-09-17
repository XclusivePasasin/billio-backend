from flask import Blueprint, request, jsonify
from ..models.user_model import User
from .. import db
import bcrypt
from datetime import datetime

users_bp = Blueprint('users', __name__)

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    usuario = data.get('usuario')
    clave = data.get('clave')
    
    # Verificar si el correo ya existe
    if User.query.filter_by(correo=correo).first():
        return jsonify({"error": "El correo ya está en uso"}), 400

    # Verificar si el nombre de usuario ya existe
    if User.query.filter_by(usuario=usuario).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    # Hashear la contraseña
    password_hash = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Crear nuevo usuario
    new_user = User(nombre=nombre, apellido=apellido, correo=correo, usuario=usuario, clave=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@users_bp.route('/update_user', methods=['PUT'])
def update_user():
    data = request.json
    user_id = data.get('id')  # Se obtiene el id del usuario

    # Verificar si el usuario existe por id
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Actualizar los campos (excepto id y tipo)
    if data.get('nombre'):
        user.nombre = data['nombre']
    if data.get('apellido'):
        user.apellido = data['apellido']
    if data.get('correo'):
        user.correo = data['correo']
    if data.get('usuario'):
        user.usuario = data['usuario']
    if data.get('clave'):
        password_hash = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.clave = password_hash
    if data.get('estado'):
        user.estado = data['estado']

    db.session.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


@users_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    user_id = data.get('id')  # Se obtiene el id del usuario

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Eliminar el usuario
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

# Ruta para iniciar sesión
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    correo_o_usuario = data.get('correo_o_usuario')
    clave = data.get('clave')

    # Buscar por correo o nombre de usuario
    user = User.query.filter((User.correo == correo_o_usuario) | (User.usuario == correo_o_usuario)).first()

    if not user:
        return jsonify({"error": "Correo o nombre de usuario incorrecto"}), 401

    # Verificar la contraseña
    if bcrypt.checkpw(clave.encode('utf-8'), user.clave.encode('utf-8')):
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401

# Ruta para cerrar sesión
@users_bp.route('/logout', methods=['POST'])
def logout():
    data = request.json
    user_id = data.get('id')

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"message": "Cierre de sesión exitoso"}), 200