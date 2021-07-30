from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    contact_number = db.Column(db.String(10))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(260))
    pan_card = db.Column(db.String(10))
    current_location = db.Column(db.String(200))
    candidate_compensation = db.relationship('CandidateCompensation', backref='candidate', uselist=False)  # one to
    # one with candidate compensation
    candidate_professions = db.relationship('CandidateProfession', backref='candidate')  # one to many with candidate
    # profession
    candidate_educations = db.relationship('CandidateEducation', backref='candidate')  # one to many w education
    applications = db.relationship('Application', backref='candidate')

    def __repr__(self):
        return 'id: ' + str(self.id) + ', name:' + str(self.first_name + ' ' + self.last_name)


class CandidateCompensation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expected_ctc = db.Column(db.Float(3))
    current_ctc = db.Column(db.Float(3))
    notice_period = db.Column(db.Integer)
    buyout_option = db.Column(db.String(5))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # one to one relationship with candidate


class CandidateProfession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    years_of_experience = db.Column(db.String(20))
    company_name = db.Column(db.String(100))
    work_location = db.Column(db.String(20))
    current_designation = db.Column(db.String(20))
    key_skill_sets = db.Column(db.String(20))
    linkedin_profile = db.Column(db.String(20))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # many to one with candidate


class CandidateEducation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_board = db.Column(db.String(30))
    school_completion = db.Column(db.Integer)
    school_percentage = db.Column(db.Float(3))
    school_cgpa = db.Column(db.Float(3))
    school_name = db.Column(db.String(30))
    school_place = db.Column(db.String(30))
    intermediate_degree = db.Column(db.String(30))
    intermediate_completion = db.Column(db.Integer)
    intermediate_percentage = db.Column(db.Float(3))
    intermediate_cgpa = db.Column(db.Float(3))
    intermediate_college = db.Column(db.String(30))
    intermediate_place = db.Column(db.String(30))
    graduation_degree = db.Column(db.String(10))
    graduation_completion = db.Column(db.Integer)
    graduation_percentage = db.Column(db.Float(3))
    graduation_cgpa = db.Column(db.Float(3))
    graduation_college = db.Column(db.String(30))
    graduation_place = db.Column(db.String(30))
    postgraduation_degree = db.Column(db.String(10))
    postgraduation_completion = db.Column(db.Integer)
    postgraduation_percentage = db.Column(db.Float(3))
    postgraduation_cgpa = db.Column(db.Float(3))
    postgraduation_college = db.Column(db.String(30))
    postgraduation_place = db.Column(db.String(30))

    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # many to one with candidate


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    contact_number = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    position = db.Column(db.String(20))
    role = db.Column(db.String(20))
    recruiter = db.relationship('Recruiter', backref='employee', uselist=False)
    interviewer = db.relationship('Interviewer', backref='employee', uselist=False)
    manager = db.relationship('Manager', backref='employee', uselist=False)

    def __repr__(self):
        return 'id: ' + str(self.id) + ', name: ' + str(self.first_name) + ' ' + str(self.last_name) + ', role: ' + str(
            self.role)


class Interviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee
    interviews = db.relationship('Interview', backref='interviewer')  # one to many relation with interview

    def __repr__(self):
        return 'id: ' + str(self.id) + ', emp id: ' + str(self.employee_id)


class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.Date)
    round = db.Column(db.Integer)
    meet_link = db.Column(db.String(50))
    feedback = db.Column(db.String(500))
    next_round = db.Column(db.Boolean)
    is_done = db.Column(db.Boolean)
    interviewer_id = db.Column(db.Integer, db.ForeignKey('interviewer.id'))  # many to one w interviewer
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))  # many to one w recruiter
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))  # many to one with application

    def __repr__(self):
        return 'id: ' + str(self.id) + ', start_time: ' + str(self.start_time) + ', end time: ' + str(
            self.end_time) + ', date: ' + str(self.date) + ', candidate_id: ' + str(
            self.candidate_id) + ', interviewer id: ' + str(self.interviewer_id) + ', recruiter id:' + str(
            self.recruiter_id) + ', job: ' + str(self.position_id)


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee

    def __repr__(self):
        return 'id: ' + str(self.id) + ', employee id: ' + str(self.employee_id)


class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee
    interviews = db.relationship('Interview', backref='recruiter')  # one to many with interview. (scheduling)

    def __repr__(self):
        return 'id: ' + str(self.id) + 'employee id:' + str(self.employee_id)


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String(500))
    required_number = db.Column(db.Integer)
    number_applied = db.Column(db.Integer)
    applications = db.relationship('Application', backref='application')

    def __repr__(self):
        return 'id: ' + str(self.id) + ', title: ' + self.title


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    round = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10))
    Feedback = db.Column(db.String(255))
    push = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'id: ' + str(self.id) + ', pos id:' + str(self.position_id) + ', candidate id: ' + str(self.candidate_id)
#
# class Interview_Feedback_Forms(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
#     file =