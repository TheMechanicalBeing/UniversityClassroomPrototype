from flask import Flask

from src.config import Config
from .models import db, Person
from src.views import main_bp, auth_bp


BLUEPRINTS = [main_bp, auth_bp]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_blueprints(app)

    return app


def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
