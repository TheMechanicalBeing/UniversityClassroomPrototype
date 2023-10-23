from flask import Blueprint, render_template, redirect, url_for, g, session, flash, current_app
import requests
from sqlalchemy import text
from ..forms import LoginForm
from .. import db
from ..extensions import bcrypt, tagnames
import functools

login = Blueprint('login', __name__, url_prefix="/auth", template_folder="/templates/forms")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.person is None:
            flash("You must be logged in to use that URL!")
            return redirect(url_for("main.home"))

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.person.get("role_id") != 1:
            flash("You do not have permission to go to this URL!")
            return redirect(url_for("main.home"))

        return view(**kwargs)

    return wrapped_view


@login.get("/login")
def login_get():
    if g.person:
        return redirect(url_for("main.home"))
    form = LoginForm()
    return render_template("login.html", title="login", form=form, tagnames=tagnames)


@login.post("/login")
def login_post():
    response = requests.get("http://localhost:5000/api/people")
    form = LoginForm()
    if form.validate_on_submit():
        current_person = next((person for person in response.json() if person.get("email") == form.email.data), None)
        if current_person and bcrypt.check_password_hash(current_person.get("password"), form.password.data):
            session.clear()
            session["person_id"] = current_person.get("id")
            return redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessfull. Please check email or password if is written correctly.")
    return redirect(url_for("login.login_get"))


@login.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
