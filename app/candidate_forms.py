from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, RadioField, ValidationError, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import Candidate, CollegeList



class CandidateRegistrationForm(FlaskForm):
    #username = StringField('username', validators=[DataRequired(), Length(min=1, max = 20)])
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    create_password = PasswordField('Create Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('create_password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Candidate.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This Email Id is already in use!!')



class CandidateLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class CandidatePersonalDetails(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Id', validators=[DataRequired(), Email()])
    contact = StringField('Contact', validators=[DataRequired()])
    current_location = TextAreaField('Residential Address(Optional)', validators=[DataRequired()])
    pancard = StringField('Pan Card', validators=[DataRequired()])
    submit = SubmitField('Next')

class CandidateEducationDetails(FlaskForm):
    schoolboard = SelectField('Board Name', validators=[DataRequired()],
                               choices=['','SSC', 'CBSE', 'ICSE', 'Others'])
    schoolcompletion = IntegerField('Year of Completion', validators=[DataRequired()])
    schoolpercentage = StringField('Percentage', validators=[DataRequired()])
    schoolcgpa = StringField('CGPA(Out of 10)', validators=[DataRequired()])
    schoolname = StringField('School Name', validators=[DataRequired()])
    schoolplace = StringField('Place/Location', validators=[DataRequired()])

    intermediatedegree = SelectField('Name of the Degree', validators=[DataRequired()],
                               choices=['','Intermediate', 'Diploma', 'Others'])
    intermediatecompletion = IntegerField('Year of Completion', validators=[DataRequired()])
    intermediatepercentage = StringField('Percentage', validators=[DataRequired()])
    intermediatecgpa = StringField('CGPA(Out of 10)', validators=[DataRequired()])
    intermediatecollege = StringField('School/College', validators=[DataRequired()])
    intermediateplace = StringField('Place/Location', validators=[DataRequired()])

    graduationdegree = SelectField('Name of the Degree', validators=[DataRequired()],
                                     choices=['','B.Tech', 'B.E', 'B.Sc', 'Others'])
    graduationcompletion = IntegerField('Year of Completion', validators=[DataRequired()])
    graduationpercentage = StringField('Percentage', validators=[DataRequired()])
    graduationcgpa = StringField('CGPA(Out of 10)', validators=[DataRequired()])
    graduationcollege = SelectField('Name of the College', validators=[DataRequired()],
                                   choices=[graduationcollege.collegename for graduationcollege in CollegeList.query.all()])
    graduationplace = StringField('Place/Location', validators=[DataRequired()])

    postgraduationdegree = SelectField('Name of the Degree', validators=[DataRequired()],
                                   choices=['','M.Tech', 'M.E', 'M.Sc', 'Others'])
    postgraduationcompletion = IntegerField('Year of Completion', validators=[DataRequired()])
    postgraduationpercentage = StringField('Percentage', validators=[DataRequired()])
    postgraduationcgpa = StringField('CGPA(Out of 10)', validators=[DataRequired()])
    postgraduationcollege = SelectField('Name of the College', validators=[DataRequired()],
                                  choices=[postgraduationcollege.collegename for postgraduationcollege in CollegeList.query.all()])

    postgraduationplace = StringField('Place/Location', validators=[DataRequired()])
    next = SubmitField('Next')


class CandidateProfessionDetails(FlaskForm):
    currentdesignation = StringField('Current Designation', validators=[DataRequired()])
    yearsofexperience = SelectField('Years of Experience', validators=[DataRequired()],
                                    choices=['', '0-1 Years', '1-3 Years', '3-5 Years', '5-8 Years', '8-12 Years',
                                             '12-15 Years', '15+ Years'])
    companyname = TextAreaField('Company Name', validators=[DataRequired()])
    location = StringField('Work Location', validators=[DataRequired()])
    keyskillsets = TextAreaField('Key Skill Sets', validators=[DataRequired()])
    linkedinprofile = StringField('LinkedIn Profile(Optional)', validators=[DataRequired()])
    submit = SubmitField('Next')


class CandidateCompensationDetails(FlaskForm):
    currentctc = FloatField('Current CTC', validators=[DataRequired()])
    expectedctc = FloatField('Expected CTC', validators=[DataRequired()])
    noticeperiod = IntegerField('Notice Period', validators=[DataRequired()])
    buyoutoption = RadioField('Buyout Option', validators=[DataRequired()])
    submit = SubmitField('Submit')




