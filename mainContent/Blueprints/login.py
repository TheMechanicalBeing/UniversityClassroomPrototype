from flask import Blueprint, render_template, redirect, url_for

from ..forms import LoginForm
from pathlib import Path

login = Blueprint('login', __name__, url_prefix="/auth", template_folder="/templates/forms")


@login.get("/login")
def login_get():
    print(Path(__file__))
    form = LoginForm()
    return render_template("login.html", title="login", form=form)


@login.post("/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("main.home"))
    return redirect(url_for("login.login_get"))


@login.route("/logout")
def logout():
    return redirect(url_for("main.home"))
