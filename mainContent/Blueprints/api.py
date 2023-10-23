from flask import Blueprint, jsonify, request
import requests
import re
from flask_bcrypt import Bcrypt
from sqlalchemy import text
from ..models import db, Person, Administrator, Student, Lecturer


api = Blueprint("api", __name__, url_prefix="/api", template_folder="/templates")


@api.get("/people")
def get_people():
    people = db.session.execute(text("SELECT * FROM people")).fetchall()
    to_return = [
        {
            "id": person[0],
            "role_id": person[1],
            "name": person[2],
            "surname": person[3],
            "email": person[4],
            "password": person[5],
            "bio": person[6]
        }
        for person in people
    ]
    return jsonify(to_return)


@api.get("/people/<int:current_id>")
def get_person(current_id):
    api_url = "http://localhost:5000/api/people"
    response = requests.get(api_url)
    if response.status_code == 200:
        to_return = next((item for item in response.json() if item["id"] == current_id), None)
        return to_return if to_return else {"Message": "This user does not exist."}
    else:
        return jsonify({"Message": "There was an error",
                        "Error Code": response.status_code})


@api.put("/people/<int:current_id>")
def put_person(current_id):
    person = Person.query.get_or_404(current_id)
    if person and request.content_type == "application/json":
        allowed_to_change = ["name", "surname", "password"]
        data = request.get_json()
        endswith = person.email[len(person.name)+len(person.surname)+1:]
        if "name" in data.keys():
            person.name = data["name"].capitalize()
        if "surname" in data.keys():
            person.surname = data["surname"].capitalize()
        if "password" in data.keys():
            person.password = Bcrypt().generate_password_hash(data["password"]).decode("utf-8")
        person.email = data.get("name", person.name) + "." + data.get("surname", person.surname) + endswith

        return jsonify({
            "message": "Updated person's info successfully!",
            "person": {
                "id": person.id,
                "role_id": person.role_id,
                "name": person.name,
                "surname": person.surname,
                "email": person.email,
                "password": person.password
            }
        })
    else:
        return jsonify({"message": "There was an error updating person's data"})


@api.delete("/people/<int:current_id>")
def delete_person(current_id):
    person = Person.query.get_or_404(current_id)
    if person:
        match person.role_id:
            case 1:
                role = Administrator.query.get_or_404(person.administrators[0].id)
            case 2:
                role = Lecturer.query.get_or_404(person.lecturers[0].id)
            case 3:
                role = Student.query.get_or_404(person.students[0].id)
        db.session.delete(role)
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted successfully."})
    else:
        return jsonify({"message": "Could not find person!"})


@api.post("/people")
def post_add_someone():
    if request.content_type == "application/json":
        data = request.get_json()

        role_converter = {
            1: "administrator",
            2: "lecturer",
            3: "student"
        }

        role_id = data.get("role_id")
        name = data.get("name")
        surname = data.get("surname")
        match role_id:
            case 1:
                endswith = "uni.staff.ge"
            case 2:
                endswith = "uni.edu.ge"
            case 3:
                endswith = "uni.stud.edu.ge"

        email = f'{name}.{surname}@{endswith}'.replace(" ", "")
        current_table = role_converter[role_id] + "s"

        with db.engine.connect() as connection:
            email_query = text("SELECT id FROM people WHERE email REGEXP :pattern")
            emails = connection.execute(email_query, {"pattern": f"{name}\.{surname}.*@{endswith}".replace(" ", "")}).fetchall()
        if emails:
            email = f'{name}.{surname}.{len(emails)}@{endswith}'

        db.session.execute(text(
            "INSERT INTO people (role_id, name, surname, email, password) values ({}, '{}', '{}', '{}', '{}')".format(role_id, name.capitalize(), surname.capitalize(), email, Bcrypt().generate_password_hash(data.get("password")).decode("utf-8"))))

        new_person = db.session.execute(text(" SELECT * FROM people WHERE email = '{}'".format(email))).fetchone()

        db.session.execute(text("INSERT INTO {} (person_id) values ({})".format(
            current_table,
            new_person[0]
        )))

        db.session.commit()

        return jsonify({
            "message": f"Person and {role_converter[role_id].capitalize()} added successfully",
            "Person": {
                "id": new_person[0],
                "role_id": new_person[1],
                "name": new_person[2],
                "surname": new_person[3],
                "email": new_person[4],
                "password": new_person[5],
            }
        })
    else:
        return jsonify({"message": "There was en error adding user!",})
