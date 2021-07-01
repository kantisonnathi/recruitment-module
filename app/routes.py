from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm, InterviewForm
from app.models import Employee, Candidate, Interview, Interviewer


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "Manager":
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('manager_candidates.html', candidates=candidates)
        else:
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('manager_candidates.html',candidates = candidates)
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and employee.password == form.password.data:
            login_user(employee)
            if current_user.role == "Manager":
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('manager_candidates.html',candidates = candidates)
            else:
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('manager_candidates.html',candidates = candidates)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/interview/new/<candidate_id_str>', methods=['GET', 'POST'])
def createNewCandidate(candidate_id_str):
    candidate = Candidate.query.filter_by(id=candidate_id_str).first()
    print(candidate)
    interviewers = Employee.query.filter_by(role='Interviewer').all()
    print(interviewers[0].first_name)
    form = InterviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        interview = Interview()
        interviewer_id = request.form.get('interviewer')
        print(interviewer_id)
        print(form.date.data)
        print(form.start_time.data)
        print(form.end_time.data)
        print(form.round.data)
        print(form.meet_link.data)
    return render_template('new_interview.html', title='Schedule Interview', form=form, interviewers=interviewers)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
