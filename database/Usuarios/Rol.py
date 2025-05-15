from src.db_connection import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_rol = db.Column(db.String(20), nullable=False)
