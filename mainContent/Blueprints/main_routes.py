from flask import Blueprint, render_template, g, session
from ..extensions import tagnames


main = Blueprint("main", __name__, template_folder="/templates")


@main.get("/")
@main.get("/home")
def home():
    return render_template("home.html", title="Home", tagnames=tagnames)
