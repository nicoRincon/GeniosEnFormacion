from src.db_connection import db
from datetime import datetime, timezone



class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_contenido = db.Column(db.Integer, db.ForeignKey('contenido.id'), nullable=False)
    titulo = db.Column(db.String(50), nullable=False)
    tipo_evaluacion = db.Column(db.String(10), nullable=False)
    lista_preguntas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))