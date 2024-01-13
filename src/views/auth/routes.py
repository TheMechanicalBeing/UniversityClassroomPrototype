from os import path
from flask import Blueprint, render_template, redirect, url_for

from src.views.auth.forms import LoginForm


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.get("/login")
def login_get():
    form = LoginForm()
    return render_template("auth/login.html", title="login", form=form)


@auth_bp.post("/login")
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("main_bp.home"))
    return redirect(url_for("login.login_get"))


@auth_bp.route("/logout")
def logout():
    return redirect(url_for("main.home"))
