from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm, InterviewForm, ManagerFeedbackForm
from app.models import Employee, Candidate, Interview, Interviewer

# candidate forms
#from app.candidate_forms import CandidateRegistrationForm, CandidateLoginForm, CandidatePersonalDetails



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


# manager routes

@app.route("/final_selected_candidates")
def final_selected_candidates():
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('final_selected_candidates.html', candidates=candidates)


@app.route('/info/<int:candidate_id>')
def info(candidate_id):
    cur_candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('candidate_info.html', cur_candidate=cur_candidate)

@app.route('/candidate_interviews/<int:candidate_id>')
def candidate_interviews(candidate_id):
    interviews = Interview.query.filter_by(candidate_id = candidate_id)
    cur_candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('interview_info.html', interviews=interviews,cur_candidate=cur_candidate)


@app.route('/manager_feedback')
def manager_feedback():
    form = ManagerFeedbackForm()
    return render_template('manager_feedback.html',form=form)


# candidate routes

# candidate application link
@app.route('/application-form', methods=['GET','POST'])
def application():
    form = CandidatePersonalDetails()
    return render_template('candidate_application.html', title='application', form=form)


# candidate login link
@app.route('/candidate-login', methods=['GET', 'POST'])
def candidateLogin():
    form=CandidateLoginForm()
    if form.validate_on_submit():
        return redirect(url_for('application'))
    return render_template('candidate_login.html', title='candidateLogin', form=form)

#candidate Registration link
@app.route('/candidate-registration', methods=['GET', 'POST'])
def candidateRegister():
    form = CandidateRegistrationForm()
    if request.method=='POST':
        return redirect(url_for('candidateLogin'))
    return render_template('candidate_registration.html', title='candidateRegister', form=form)

