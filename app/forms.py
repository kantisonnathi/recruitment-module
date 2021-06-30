from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Employee, Candidate
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email')  # pass in validators later
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



