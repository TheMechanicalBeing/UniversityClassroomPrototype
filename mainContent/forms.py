from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class AddSomeone(FlaskForm):
    name = StringField("First Name", validators=[DataRequired()])
    surname = StringField("Last Name", validators=[DataRequired()])
    role = SelectField("Role", validators=[DataRequired()], choices=[("administrator", "Administrator"), ("lecturer", "Lecturer"), ("student", "Student")])
    submit = SubmitField("Add")
