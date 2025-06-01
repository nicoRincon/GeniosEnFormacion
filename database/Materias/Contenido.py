from src.db_connection import db
from datetime import datetime, timezone



class Contenido(db.Model):
    __tablename__ = 'contenido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tema = db.Column(db.Integer, db.ForeignKey('temas.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    nivel_grado = db.Column(db.Numeric)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    tema = db.relationship('Tema', back_populates='contenidos')
    actividades = db.relationship('Actividad', back_populates='contenido_relacionado')
    notas_contenido = db.relationship('NotaContenido', back_populates='contenido')