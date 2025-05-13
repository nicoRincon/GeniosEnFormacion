from werkzeug.security import check_password_hash, generate_password_hash
import json
from flask import session
from flask import Flask
from flask_migrate import Migrate
from src.db_connection import db, init_db

class User:
    user_json_file = 'users.json'

    def __init__(self, username: str, password: str, confirm_password: str = ''):
        self.username = username
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

            users = {}

            with open('users.json', 'r') as file:
                users = json.load(file)

            if self.username in users:
                raise ValueError('El usuario ya existe')

            users[self.username] = {'password': hashed_password}

            with open(self.user_json_file, 'w') as file:
                json.dump(users, file)
        else:
            raise ValueError('Las contraseñas no coinciden')

