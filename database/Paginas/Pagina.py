from src.db_connection import db
from datetime import datetime, timezone


class Pagina(db.Model):
    __tablename__ = 'paginas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tipo_pagina = db.Column(db.Integer, db.ForeignKey('tipos_pagina.id'), nullable=False)
    id_pagina_padre = db.Column(db.Integer, db.ForeignKey('paginas.id'), nullable=True)
    nombre_pagina = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(80))
    ruta = db.Column(db.String(50), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    rol_paginas = db.relationship('RolPagina', back_populates='pagina')
    subpaginas = db.relationship('Pagina', backref=db.backref('padre', remote_side=[id]))