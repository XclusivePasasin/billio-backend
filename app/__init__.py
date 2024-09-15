from flask import Flask
from .routes.users import users_bp  # Importar el blueprint de users

def create_app():
    app = Flask(__name__)

    # Registrar el blueprint de usuarios
    app.register_blueprint(users_bp, url_prefix='/users')

    return app
