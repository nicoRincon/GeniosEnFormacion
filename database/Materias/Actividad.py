from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Actividad(db.Model):
    __tablename__ = 'actividades'
    id = db.Column(db.Integer, primary_key=True)
    id_contenido = db.Column(db.Integer, db.ForeignKey('contenido.id'), nullable=False)
    id_tipo_actividad = db.Column(db.Integer, db.ForeignKey('tipo_actividad.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))