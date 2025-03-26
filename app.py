from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from structures.crud import crud_api
from config import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)  # Привязываем db к app
    from structures.views import views  # Импортируем Blueprint
    app.register_blueprint(views)
    with app.app_context():  # Создаем контекст перед db.create_all()
        db.create_all()
    return app

app = create_app()
app.register_blueprint(crud_api, url_prefix='/structures/api/v1')
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)