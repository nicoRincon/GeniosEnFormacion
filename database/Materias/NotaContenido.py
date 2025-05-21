from src.db_connection import db
from datetime import datetime, timezone



class NotaContenido(db.Model):
    __tablename__ = 'notas_x_contenido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_contenido = db.Column(db.Integer, db.ForeignKey('contenido.id'), nullable=False)
    nota_obtenida = db.Column(db.Numeric)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))