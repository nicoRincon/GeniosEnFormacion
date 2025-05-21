from src.db_connection import db
from datetime import datetime, timezone



class Recurso(db.Model):
    __tablename__ = 'recursos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_actividad = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    contenido = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))