import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///structure.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False