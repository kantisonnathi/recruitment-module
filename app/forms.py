import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Employee, Candidate
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email')  # pass in validators later
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class InterviewForm(FlaskForm):
    start_time = TimeField('Start time')
    end_time = TimeField('End time')
    date = DateField('Date', validators=[DataRequired()], default=datetime.date.today(), format='%d-%m-%Y')
    round = IntegerField('Round')
    meet_link = StringField('Meet link')
    submit = SubmitField('Submit')

