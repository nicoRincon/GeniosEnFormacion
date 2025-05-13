from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.String(20), primary_key=True)
    nombre_rol = db.Column(db.String(20), nullable=False)
