from src.db_connection import db

class RolPagina(db.Model):
    __tablename__ = 'roles_x_pagina'
    id_rol = db.Column(db.Integer(), db.ForeignKey('roles.id'), primary_key=True)
    id_pagina = db.Column(db.Integer, db.ForeignKey('paginas.id'), primary_key=True)

    rol = db.relationship('Rol', back_populates='rol_paginas')
    pagina = db.relationship('Pagina', back_populates='rol_paginas')