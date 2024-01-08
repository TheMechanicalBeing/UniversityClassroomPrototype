from flask import Flask

from mainContent.config import Config
from .models import db, Person
from .extensions import tagnames
from .Blueprints import main, login


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main)
    app.register_blueprint(login)

    return app
