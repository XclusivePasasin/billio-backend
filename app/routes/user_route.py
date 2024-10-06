from flask import Blueprint, request, jsonify
from ..models.user_model import User
from .. import db
import bcrypt
from datetime import datetime
import re

users_bp = Blueprint('users', __name__)
# Ruta para obtener a un usuario por su nombre de usaurio o correo
@users_bp.route('/get_user', methods=['POST'])
def get_users():
    try:
        # Consultar todos los usuarios directamente sin necesidad de parámetros
        users = User.query.all()

        if not users:
            return jsonify({"message": "No se encontraron usuarios"}), 404

        # Crear una lista con los datos de todos los usuarios
        users_list = [{
            "id": user.id,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "correo": user.correo,
            "usuario": user.usuario,
            "tipo": user.tipo,
            "estado": user.estado
        } for user in users]

        # Devolver la lista de usuarios
        return jsonify(users_list), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@users_bp.route('/get_user_login', methods=['POST'])
def get_user_by_identifier():
    data = request.json
    identifier = data.get('correo') or data.get('usuario')  # Asegúrate de obtener el identifier correctamente

    if not identifier:
        return jsonify({"error": "Se requiere 'correo' o 'usuario' en el cuerpo de la solicitud"}), 400

    try:
        user = User.query.filter((User.correo == identifier) | (User.usuario == identifier)).first()

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "data":[
                { 
                    "id": user.id,
                    "nombre": user.nombre,
                    "apellido": user.apellido,
                    "correo": user.correo,
                    "usuario": user.usuario,
                    "clave": user.clave,
                    "estado": user.estado}
            ]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Regex para validaciones
email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
username_regex = re.compile(r'^(?!.*[_.]{2})[a-zA-Z0-9._]{4,30}$')
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo')
    usuario = data.get('usuario')
    clave = data.get('clave')
    
    # Validación de nombre
    if not nombre or not re.match(r'^[a-zA-Z\s-]{2,50}$', nombre):
        return jsonify({"error": "El nombre debe tener entre 2 y 50 caracteres y solo contener letras."}), 400
    
    # Validación de apellido
    if not apellido or not re.match(r'^[a-zA-Z\s-]{2,50}$', apellido):
        return jsonify({"error": "El apellido debe tener entre 2 y 50 caracteres y solo contener letras."}), 400
    
    # Validación de correo
    if not correo or not email_regex.match(correo):
        return jsonify({"error": "El correo debe ser válido."}), 400
    
    # Verificar si el correo ya existe
    if User.query.filter_by(correo=correo).first():
        return jsonify({"error": "El correo ya está en uso"}), 400

    # Verificar si el nombre de usuario ya existe
    if User.query.filter_by(usuario=usuario).first():
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400
    
     # Validación de contraseña
    if not clave or not password_regex.match(clave):
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, minúscula, número y carácter especial."}), 400

    # Hashear la contraseña
    password_hash = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Crear nuevo usuario
    new_user = User(nombre=nombre, apellido=apellido, correo=correo, usuario=usuario, clave=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201

@users_bp.route('/update_user', methods=['POST'])
def update_user():
    data = request.json
    user_id = data.get('id')  # Se obtiene el id del usuario

    # Verificar si el usuario existe por id
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Validar si el correo ya está registrado por otro usuario solo si el correo ha cambiado
    nuevo_correo = data.get('correo')
    if nuevo_correo and nuevo_correo != user.correo:
        correo_existente = User.query.filter(User.correo == nuevo_correo, User.id != user_id).first()
        if correo_existente:
            return jsonify({"error": "El correo ya está registrado"}), 400

    # Validar si el nombre de usuario ya está registrado por otro usuario solo si el nombre de usuario ha cambiado
    nuevo_usuario = data.get('usuario')
    if nuevo_usuario and nuevo_usuario != user.usuario:
        usuario_existente = User.query.filter(User.usuario == nuevo_usuario, User.id != user_id).first()
        if usuario_existente:
            return jsonify({"error": "El nombre de usuario ya está registrado"}), 400

    # Validar la contraseña solo si se envía una nueva clave
    nueva_clave = data.get('clave')
    if nueva_clave:
        # Validar si la clave cumple con el regex
        if not password_regex.match(nueva_clave):
            return jsonify({"error": "La contraseña no cumple con los requisitos de seguridad"}), 400
        # Si la clave es válida, se realiza el hash y se actualiza
        password_hash = bcrypt.hashpw(nueva_clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.clave = password_hash

    # Actualizar los campos (excepto id y tipo)
    if data.get('nombre'):
        user.nombre = data['nombre']
    if data.get('apellido'):
        user.apellido = data['apellido']
    if data.get('correo'):
        user.correo = data['correo']
    if data.get('usuario'):
        user.usuario = data['usuario']
    if data.get('estado'):
        user.estado = data['estado']

    db.session.commit()

    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

@users_bp.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    user_id = data.get('id')

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

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
