from app import db


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    contact_number = db.Column(db.String(10))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    pan_card = db.Column(db.String(10))
    current_location = db.Column(db.String(20))
    status = db.Column(db.String(10))


class CandidateCompensation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expected_ctc = db.Column(db.Float(3))
    current_ctc = db.Column(db.Float(3))
    notice_period = db.Column(db.Integer())
    buyout_option = db.Column(db.Boolean)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # one to one relationship with candidate


class CandidateProfession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    years_of_experience = db.Column(db.Integer)
    company_name = db.Column(db.String(20))
    location = db.Column(db.String(20))
    position = db.Column(db.String())
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # many to one with candidate


class CandidateEducation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(40))
    start_year = db.Column(db.String(4))
    end_year = db.Column(db.String(4))
    description = db.Column(db.String(200))
    cgpa = db.Column(db.Float(2))
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # many to one with candidate


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    contact_number = db.Column(db.String(10))
    email = db.Column(db.String(100))
    password = db.Column(db.String(255))
    position = db.Column(db.String(20))
    role = db.Column(db.String(20))


class Interviewer(db.Model):
    # one to many relation with interview
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee


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
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))  # many to one w candidate
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'))  # many to one w recruiter


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee


class Recruiter(db.Model):
    # one to many with interview. (scheduling)
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))  # one to one with employee











