from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class CandidateRegistrationForm(FlaskForm):
    #username = StringField('username', validators=[DataRequired(), Length(min=1, max = 20)])
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    create_password = PasswordField('Create Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class CandidateLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    #signup = SelectField('Sign Up')


class CandidateApplicationDetails(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[DataRequired()])
    residential_address = TextAreaField('Residential Address(Optional)', validators=[DataRequired()])
    pancard = StringField('Pan Card', validators=[DataRequired()])
    institutename = StringField('Institute Name', validators=[DataRequired()])
    instituteplace = StringField('Place/Location', validators=[DataRequired()])
    nameofthedegree = StringField('Name of the Degee', validators=[DataRequired()])
    percentage = StringField('percentage/CGPA', validators=[DataRequired()])
    currentposition = StringField('Current Position', validators=[DataRequired()])
    yearsofexperience = IntegerField('Years of Experience', validators=[DataRequired()])
    companyname = TextAreaField('Company Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    skillsets = TextAreaField('Skill Sets', validators=[DataRequired()])
    linkedinprofile = StringField('LinkedIn Profile(Optional)', validators=[DataRequired()])
    expectedctc = FloatField('Expected CTC', validators=[DataRequired()])
    currentctc = FloatField('Current CTC', validators=[DataRequired()])
    noticeperiod = IntegerField('Notice Period', validators=[DataRequired()])
    buyoutoption = RadioField('Buyout Option', validators=[DataRequired()])
    submit = SubmitField('Apply')
