from werkzeug.security import check_password_hash, generate_password_hash
import json
from flask import session
from src.db_connection import db
from database.Usuarios.Usuario import Usuario

class User:
    user_json_file = 'users.json'

    def __init__(
        self,
        username: str,
        password: str,
        confirm_password: str = '',
        name: str = '',
        last_name: str = '',
        email: str = '',
        role: int = 1,
    ):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.role = role

    def __repr__(self):
        return f"User({self.username}, {self.password})"

    def login(self):
        user: Usuario = (
            db.session
                .query(Usuario)
                .filter(Usuario.nombre_usuario == self.username)
                .with_entities(
                    Usuario.id,
                    Usuario.nombre_usuario,
                    Usuario.clave,
                    Usuario.nombre,
                    Usuario.apellido,
                )
                .first()
        )

        if user and check_password_hash(
            user.clave, self.password
        ):
            session['username'] = self.username
            session['user_id'] = user.id
            session['complete_name'] = f"{user.nombre} {user.apellido}"
        else:
            raise ValueError('Usuario o contraseña incorrectos')

    def logout(self):
        session.clear()

    def register(self):
        if self.password == self.confirm_password:
            hashed_password = generate_password_hash(self.password)

            user_found = (
                db.session
                    .query(Usuario)
                    .filter(Usuario.nombre_usuario == self.username)
                    .first()
            )
            if user_found:
                raise ValueError('El usuario ya existe')

            user = Usuario()
            user.nombre = self.name
            user.apellido = self.last_name
            user.nombre_usuario = self.username
            user.correo = self.email
            user.clave = hashed_password
            user.id_rol = self.role
            db.session.add(user)
            db.session.commit()
        else:
            raise ValueError('Las contraseñas no coinciden')

