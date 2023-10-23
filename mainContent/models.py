from sqlalchemy import PrimaryKeyConstraint
from .extensions import db


"""
Model Needs:
* Person -> name, surname, email, role_id 
* role_id Definition:
0 - no role (Default) (Avoid to use that)
1 - Administrator
2 - Lecturer
3 - Student
* Person -> [Administrator, Lecturer, Student] COMMENT Person is base class, for storing common columns
One-to-many relationship
* Administrator COMMENT It has role of staff;
F.E. add/delete faculty, add/delete lecturer or add/delete student;
So this database is not going to be massive in both columns and rowswise
* Administrator -> id, person_id
* Student -> id, person_id, course, faculty_id
* Lecturer -> id, person_id
* Group -> id, lecturer_id, subject_id
* group_id <--> student_id + score COMMENT this table is for tracking students' belonging groups and scores
* Faculty -> id, name, subject_id
* Subject -> id, name
-------------------------
P.S. You can't make Administrator, Lecturer or Student without making Person first
"""


MAX_LENGTH = 50


"""
Many-to-many relationship
Faculty must have more than one subject
subject may belong to more than one faculty 
"""
faculty_subject = db.Table(
    "faculty_subject",
    db.Column("faculty_id", db.ForeignKey("faculties.id")),
    db.Column("subject_id", db.ForeignKey("subjects.id")),
    PrimaryKeyConstraint("faculty_id", "subject_id"),
)


"""
Many-to-many relationship
Group may have more than one student
Student may have more than one group
"""
group_student = db.Table(
    "group_student",
    db.Column("group_id", db.ForeignKey("groups.id")),
    db.Column("student_id", db.ForeignKey("students.id")),
    db.Column("score", db.Integer, default=0),
    PrimaryKeyConstraint("group_id", "student_id"),
)


# This is base model for Administrator, Lecturer and Student models
class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """
    if role_id is: 
    0 - No Role (Default Value)
    1 - Administrator
    2 - Lecturer
    3 - Student
    """
    role_id = db.Column(db.Integer, default=0)
    name = db.Column(db.String(MAX_LENGTH), nullable=False)
    surname = db.Column(db.String(MAX_LENGTH), nullable=False)
    email = db.Column(db.String(MAX_LENGTH), nullable=False, unique=True)
    password = db.Column(db.String(MAX_LENGTH), nullable=False)
    bio = db.Column(db.Text, default=f"{name} {surname}")

    """
    Making one-to-many relationships in order to these three models have access to Person model
    f.e. To get name of lecturer with "lecturer_id" of 5
    """
    administrators = db.relationship("Administrator", backref="people", lazy=True)
    lecturers = db.relationship("Lecturer", backref="people", lazy=True)
    students = db.relationship("Student", backref="people", lazy=True)


class Administrator(db.Model):
    __tablename__ = "administrators"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)


class Lecturer(db.Model):
    __tablename__ = "lecturers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)

    """
    One-to-many relationship
    In order to define lecturer's groups
    """
    groups = db.relationship("Group", backref="lecturer", lazy=True)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey("faculties.id"))
    course = db.Column(db.Integer)

    # part of the table "group-student"
    groups = db.relationship("Group", secondary=group_student, backref="student")


class Faculty(db.Model):
    __tablename__ = "faculties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(MAX_LENGTH), nullable=False, unique=True)

    # part of the table "faculty_subject"
    subjects = db.relationship("Subject", secondary=faculty_subject, backref="faculty")

    """
    One-to-many relationship
    in order to define students of faculty
    """
    students = db.relationship("Student", backref="faculties", lazy=True)


class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(MAX_LENGTH), nullable=False, unique=True)
    credit = db.Column(db.Integer, nullable=False)

    # part of the table "faculty_subject"
    faculties = db.relationship("Faculty", secondary=faculty_subject, backref="subject")

    """
    One-to-many relationship
    in order to define groups of subject
    """
    groups = db.relationship("Group", backref="subjects", lazy=True)


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturers.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)

    # part of the table "group-student"
    students = db.relationship("Student", secondary=group_student, backref="group")
