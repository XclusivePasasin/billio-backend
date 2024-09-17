from .. import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(300), nullable=False)
    apellido = db.Column(db.String(300), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    usuario = db.Column(db.String(20), nullable=False)
    clave = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(1), default='A')
    tipo = db.Column(db.String(1), default='U')

    def __repr__(self):
        return f'<User {self.usuario}>'
