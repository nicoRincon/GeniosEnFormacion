from datetime import datetime, timezone
from database.Usuarios.Rol import Rol
from src.db_connection import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_rol = db.Column(db.Integer(), db.ForeignKey(Rol.id), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    clave = db.Column(db.String(256), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))