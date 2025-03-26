import os
from flask_marshmallow import Marshmallow

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///structures.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False