from src.db_connection import db
from datetime import datetime, timezone



class Tema(db.Model):
    __tablename__ = 'temas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    materia = db.relationship('Materia', back_populates='temas')