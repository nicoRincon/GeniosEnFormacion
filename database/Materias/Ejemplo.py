from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Ejemplo(db.Model):
    __tablename__ = 'ejemplos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_contenido = db.Column(db.Integer, db.ForeignKey('contenido.id'), nullable=False)
    ejemplos = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))