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
    date = DateField('Date', validators=[DataRequired()], default=datetime.date.today(), format='%d-%m-%Y')
    submit = SubmitField('Submit')


class CreateNewEmployeeForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    contact_number = StringField('Contact Number')
    email = StringField('Email')
    submit = SubmitField('Submit')


class CreateNewPositionForm(FlaskForm):
    title = StringField('Title')
    description = StringField('Description')
    required_number = IntegerField('Number of Candidates required')
    submit = SubmitField('Submit')


#manager Class
class ManagerFeedbackForm(FlaskForm):
    feedback = StringField('Feedback', validators=[DataRequired()])
    candidate_status = StringField('Status',validators=[DataRequired()])
    submit = SubmitField('Submit')