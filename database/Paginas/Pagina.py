from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Pagina(db.Model):
    __tablename__ = 'paginas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tipo_pagina = db.Column(db.String(20), db.ForeignKey('tipos_pagina.id'), nullable=False)
    id_pagina_padre = db.Column(db.Integer, db.ForeignKey('paginas.id'), nullable=True)
    nombre_pagina = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(80))
    ruta = db.Column(db.String(20))
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))