from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class RolPagina(db.Model):
    __tablename__ = 'roles_x_pagina'
    id_rol = db.Column(db.String(20), db.ForeignKey('roles.id'), primary_key=True)
    id_pagina = db.Column(db.Integer, db.ForeignKey('paginas.id'), primary_key=True)