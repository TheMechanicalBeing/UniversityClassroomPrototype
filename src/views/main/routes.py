from os import path

from flask import Blueprint, render_template


main_bp = Blueprint("main_bp", __name__)


@main_bp.get("/")
@main_bp.get("/home")
def home():
    return render_template("main/home.html", title="Home")
