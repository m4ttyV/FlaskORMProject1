import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Создаем объект db без привязки к app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///structures.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False