import datetime

from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, InterviewForm
from app.models import Employee, Candidate, Interview, Interviewer, Position

# candidate forms
from app.candidate_forms import CandidateRegistrationForm, CandidateLoginForm, CandidatePersonalDetails


# recruiter routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "Manager":
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('manager_candidates.html', candidates=candidates)
        else:
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('all_candidates.html', candidates=candidates)
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and employee.password == form.password.data:
            login_user(employee)
            if current_user.role == "Manager":
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('manager_candidates.html', candidates=candidates)
            else:
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('all_candidates.html', candidates=candidates)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/candidate/<candidate_id_str>/job/<job_id_str>/interview/new', methods=['GET', 'POST'])
def createNewInterview(candidate_id_str, job_id_str):
    candidate = Candidate.query.filter_by(id=candidate_id_str).first()
    job = Position.query.filter_by(id=job_id_str).first()
    interviewers = Employee.query.filter_by(role='Interviewer').all()
    form = InterviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        interview = Interview()
        print(request.form.get('interviewer'))
        interviewer_id = request.form.get('interviewer')
        interview.interviewer_id = interviewer_id
        interview.recruiter_id = current_user.id
        db.session.add(interview)
        db.session.commit()
        return redirect('/interview/' + str(interview.id) + '/set')
    return render_template('new_interview.html', title='Schedule Interview', form=form, interviewers=interviewers,
                           candidate=candidate, job=job)


@app.route('/interview/<interview_id>/set', methods=['GET', 'POST'])
def setInterviewTime(interview_id):
    curr_interview = Interview.query.filter_by(id=interview_id).first()
    print(curr_interview.interviewer_id)
    interviewer = Interviewer.query.filter_by(id=curr_interview.interviewer.id).first()
    interviews_by = Interview.query.filter_by(interviewer_id=interviewer.id).all()
    # assumption: assume hours start at 9 and end at 6, each interview can only be an hour long
    possible_start_times = time_population()
    for interview in interviews_by:
        curr_time = interview.start_time
        if curr_time in possible_start_times:
            possible_start_times.remove(curr_time)

    print(possible_start_times)
    return render_template('set_time_interview.html', )


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# manager routes

@app.route("/final_selected_candidates")
def final_selected_candidates():
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('final_selected_candidates.html', candidates=candidates)


# candidate routes


# candidate application link
@app.route('/application-form', methods=['GET', 'POST'])
def application():
    form = CandidatePersonalDetails()
    return render_template('candidate_application.html', title='application', form=form)


# candidate login link
@app.route('/candidate-login', methods=['GET', 'POST'])
def candidateLogin():
    form = CandidateLoginForm()
    if form.validate_on_submit():
        return redirect(url_for('application'))
    return render_template('candidate_login.html', title='candidateLogin', form=form)


# candidate Registration link
@app.route('/candidate-registration', methods=['GET', 'POST'])
def candidateRegister():
    form = CandidateRegistrationForm()
    if request.method == 'POST':
        return redirect(url_for('candidateLogin'))
    return render_template('candidate_registration.html', title='candidateRegister', form=form)


def time_population():
    list_times = []
    time = 9
    done = False
    while not done:
        list_times.append(datetime.time(time, 0, 0))
        time += 1
        if time == 13:
            time = 1
        if time == 6:
            break
    return list_times
