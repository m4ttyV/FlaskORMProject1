from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()  # Создаем объект db без привязки к app

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)  # Привязываем db к app
    from structure.views import views  # Импортируем Blueprint
    app.register_blueprint(views)
    with app.app_context():  # Создаем контекст перед db.create_all()
        db.create_all()
    return app

app = create_app()
migrate = Migrate(app, db)