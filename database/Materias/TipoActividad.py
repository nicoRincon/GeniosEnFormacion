from src.db_connection import db
from datetime import datetime 



class TipoActividad(db.Model):
    __tablename__ = 'tipo_actividad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_actividad = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Numeric)