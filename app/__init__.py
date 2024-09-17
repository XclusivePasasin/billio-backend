from flask import Flask
from .models import db
from .routes.user_route import users_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar las rutas
    app.register_blueprint(users_bp, url_prefix='/users')

    return app
