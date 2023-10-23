from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from ..extensions import tagnames
from ..forms import AddSomeone
from .. import db
from sqlalchemy import text
from .login import bcrypt, login_required, admin_required


add = Blueprint("add", __name__, url_prefix="/add", template_folder="/templates")


@add.get("/")
@login_required
@admin_required
def add_x():
    # if g.person.get("role_id", None) != 1:
    #     flash("You don't have permission to go to this URL!")
    #     return redirect(url_for("main.home"))

    return render_template("add.html", title="Add", tagnames=tagnames)


@add.get("/someone")
@login_required
@admin_required
def add_someone_get():
    if not g.get("person", None) or g.person.get("role_id", None) != 1:
        flash("You are not allowed here!")
        return redirect(url_for("main.home"))

    form = AddSomeone(role=request.args.get("role", "administrator"))
    return render_template("add_someone.html", title="Add Someone", tagnames=tagnames, form=form)


@add.post("/someone")
@login_required
@admin_required
def add_someone_post():
    if not g.get("person", None) or g.person.get("role_id", None) != 1:
        flash("You are not allowed here!")
        return redirect(url_for("main.home"))

    form = AddSomeone(role=request.args.get("role", "administrator"))
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        match form.role.data:
            # Case defines which type of role has been given to a person.
            case "administrator":
                role_to_insert = 1
                endswith = "uni.staff.ge"
            case "lecturer":
                role_to_insert = 2
                endswith = "uni.edu.ge"
            case "student":
                role_to_insert = 3
                endswith = "uni.stud.edu.ge"

        email = f'{name}.{surname}@{endswith}'.replace(" ", "")
        current_table = form.role.data + "s"

        with db.engine.connect() as connection:
            email_query = text("SELECT id FROM people WHERE email REGEXP :pattern")
            emails = connection.execute(email_query, {"pattern": f"{name}\.{surname}.*@{endswith}".replace(" ", "")}).fetchall()
        if emails:
            email = f'{name}.{surname}.{len(emails)}@{endswith}'

        db.session.execute(text(
            "INSERT INTO people (name, surname, role_id, email, password) values ('{}', '{}', {}, '{}', '{}')".format(
                name.capitalize(), surname.capitalize(), role_to_insert, email, bcrypt.generate_password_hash("Change1!").decode('utf-8'))))

        db.session.execute(text("INSERT INTO {} (person_id) values ({})".format(
            current_table,
            db.session.execute(text("SELECT id FROM people WHERE email = '{}'".format(email))).fetchone()[0]
        )))

        db.session.commit()

        flash(f"{form.role.data.capitalize()} added succesfully!")
        return redirect(url_for('main.home'))


@add.get("/faculty")
@login_required
@admin_required
def add_something_faculty():
    if not g.get("person", None) or g.person.get("role_id", None) != 1:
        flash("You are not allowed here!")
        return redirect(url_for("main.home"))

    return render_template("add_faculty.html", title="Add Faculty", tagnames=tagnames)


@add.get("/subject")
@login_required
@admin_required
def add_subject_get():
    if not g.get("person", None) or g.person.get("role_id", None) != 1:
        flash("You are not allowed here!")
        return redirect(url_for("main.home"))

    return render_template("add_someone.html", title="Add Subject", tagnames=tagnames)


@add.post("/subject")
@login_required
@admin_required
def add_subject_post():
    pass


@add.get("/group")
@login_required
@admin_required
def add_something_group():
    if not g.get("person", None) or g.person.get("role_id", None) != 1:
        flash("You are not allowed here!")
        return redirect(url_for("main.home"))

    return render_template("add_group.html", title="Add Group", tagnames=tagnames)
