from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TipoPagina(db.Model):
    __tablename__ = 'tipos_pagina'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_tipo_pagina = db.Column(db.String(20), nullable=False)