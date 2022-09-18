# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

from flask import Flask
from flask_restx import Api
from app.database import db
from app.config import Config
from app.views.directors import director
from app.views.genres import genre
from app.views.movies import movie


# функция создания основного объекта app
def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()

    return application


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def configure_app(application):
    db.init_app(application)
    api = Api(application)
    api.add_namespace(movie)
    api.add_namespace(director)
    api.add_namespace(genre)


if __name__ == '__main__':
    app = create_app(Config())
    configure_app(app)
    app.run(host="localhost", port=10001)
