"""Conexion con la base de datos MySQL usando Flask y SQLAlchemy"""
import os
from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

mySql = MySQL()
app = Flask('app')

load_dotenv('../.env')
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.secret_key = os.getenv("SESSION_SECRET_KEY")

mySql.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

__all__ = ["app", "mySql", "db"]
