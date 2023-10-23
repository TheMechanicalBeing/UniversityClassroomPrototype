from flask import Flask, session, g, flash, redirect, url_for
import functools
from sqlalchemy import text
from .models import db, Person
from .extensions import tagnames
from .Blueprints import main, api, login, add
from .Blueprints.add_routes import bcrypt


def create_app():
    app = Flask(__name__)
    # There should be a secret key it is recommended to use environment variable for SECRET_KEY's value
    app.config["SECRET_KEY"] = "SECRET"
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

    db.init_app(app=app)
    bcrypt.init_app(app=app)

    @app.before_request
    def define_current_user():
        person_id = session.get("person_id", None)

        if person_id is None:
            g.person = None
        else:
            current_person = db.session.execute(text("SELECT * FROM people WHERE id = {}".format(person_id))).fetchone()
            g.person = {
                "id": current_person[0],
                "role_id": current_person[1],
                "name": current_person[2],
                "surname": current_person[3],
                "email": current_person[4],
                "password": current_person[5],
                "bio": current_person[6]
            }

    app.register_blueprint(main)
    app.register_blueprint(add)
    app.register_blueprint(api)
    app.register_blueprint(login)

    return app
