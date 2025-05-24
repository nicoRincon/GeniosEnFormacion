from src.db_connection import db
from datetime import datetime, timezone



class UsuarioMateria(db.Model):
    __tablename__ = 'usuarios_x_materia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    usuarios = db.relationship('Usuario', back_populates='usuarioMateria')