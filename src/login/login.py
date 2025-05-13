from werkzeug.security import check_password_hash, generate_password_hash
import json
from flask import session
from src.db_connection import db
from database.Usuarios.Usuario import Usuario

class User:
    user_json_file = 'users.json'

    def __init__(self, username: str, password: str, confirm_password: str = '', name: str = '', last_name: str = ''):
        self.username = username
        self.name = name
        self.last_name = last_name

        self.password = password
        self.confirm_password = confirm_password

    def __repr__(self):
        return f"User({self.username}, {self.password})"

    def login(self):
        with open(self.user_json_file, 'r') as file:
            users = json.load(file)

        if self.username in users and check_password_hash(
            users[self.username]['password'], self.password
        ):
            session['username'] = self.username
        else:
            raise ValueError('Usuario o contraseña incorrectos')

    def logout(self):
        session.clear()

    def register(self):
        if self.password == self.confirm_password:
            hashed_password = generate_password_hash(self.password)

            user = Usuario()
            user.nombre = self.name
            user.apellido = self.last_name
            user.nombre_usuario = self.username
            user.correo = self.username
            user.clave = hashed_password
            user.id_rol = '1'
            db.session.add(user)
            db.session.commit()

            with open('users.json', 'r') as file:
                users = json.load(file)

            if self.username in users:
                raise ValueError('El usuario ya existe')

            users[self.username] = {'password': hashed_password}

            with open(self.user_json_file, 'w') as file:
                json.dump(users, file)
        else:
            raise ValueError('Las contraseñas no coinciden')

