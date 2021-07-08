import datetime

from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app, db
from app.forms import LoginForm, InterviewForm, ManagerFeedbackForm, CreateNewInterviewerForm, CreateNewPositionForm
from app.models import Employee, Candidate, Interview, Interviewer, Position

# candidate forms
from app.candidate_forms import CandidateRegistrationForm, CandidateLoginForm, CandidateApplicationDetails


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


@app.route('/candidate/<int:candidate_id>/job/<int:job_id>/interview/new', methods=['GET', 'POST'])
def createNewInterview(candidate_id, job_id):
    # TODO: need to change job id to application id whenever it's done.
    candidate = Candidate.query.filter_by(id=candidate_id).first()
    job = Position.query.filter_by(id=job_id).first()
    interviewers = Employee.query.filter_by(role='Interviewer').all()
    form = InterviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        interview = Interview()
        interviewer_id = request.form.get('interviewer')
        interview.interviewer_id = interviewer_id
        interview.recruiter_id = current_user.id
        interview.candidate_id = candidate.id
        interview.position_id = job_id
        interview.date = datetime.datetime.strptime(request.form.get('date'), "%d-%m-%Y").date()
        interview.round = request.form.get('round')
        db.session.add(interview)
        db.session.commit()
        return redirect('/interview/' + str(interview.id) + '/set')
    return render_template('new_interview.html', title='Schedule Interview', form=form, interviewers=interviewers,
                           candidate=candidate, job=job)


@app.route('/interview/<interview_id>/delete')
def delete_interview(interview_id):
    Interview.query.filter_by(id=interview_id).delete()
    db.session.commit()
    return redirect(url_for('final_selected_candidates'))


@app.route('/interview/<interview_id>/set', methods=['GET', 'POST'])
def setInterviewTime(interview_id):
    curr_interview = Interview.query.filter_by(id=interview_id).first()
    interviewer = Interviewer.query.filter_by(id=curr_interview.interviewer_id).first()
    candidate = Candidate.query.filter_by(id=curr_interview.candidate_id).first()
    job = Position.query.filter_by(id=curr_interview.position_id).first()
    interviews_by = Interview.query.filter_by(interviewer_id=interviewer.id).all()
    # assumption: assume hours start at 9 and end at 6, each interview can only be an hour long
    possible_start_times = time_population()
    for interview in interviews_by:
        curr_time = interview.start_time
        if curr_time in possible_start_times:
            possible_start_times.remove(curr_time)
    if request.method == 'POST':
        print(request.form.get('start_time'))
        start_time = datetime.datetime.strptime(request.form.get('start_time'), "%H:%M:%S").time()
        print(start_time)
        curr_interview.start_time = start_time
        end_time = datetime.time(start_time.hour+1, start_time.minute, start_time.second)
        curr_interview.end_time = end_time
        db.session.add(curr_interview)
        db.session.commit()
        return redirect('/interview/' + interview_id)
    return render_template('set_time_interview.html', candidate=candidate, job=job, interviewer=interviewer, times=possible_start_times)


@app.route('/interview/<interview_id>', methods=['GET', 'POST'])
def view_interview(interview_id):
    curr_interview = Interview.query.filter_by(id=interview_id).first()
    interviewer = Interviewer.query.filter_by(id=curr_interview.interviewer_id).first()
    interviewer_emp = Employee.query.filter_by(id=interviewer.employee_id).first()
    candidate = Candidate.query.filter_by(id=curr_interview.candidate_id).first()
    job = Position.query.filter_by(id=curr_interview.position_id).first()
    return render_template('view_interview.html', position=job, candidate=candidate, interviewer=interviewer_emp,
                           interview=curr_interview)


@app.route('/interview/all')
def view_all_interviews():
    candidate_list = {}
    interviewer_list = {}
    interviews = Interview.query.all()
    for interview in interviews:
        current_candidate = Candidate.query.filter_by(id=interview.candidate_id).first()
        print(current_candidate)
        current_interviewer = Interviewer.query.filter_by(id=interview.interviewer_id).first()
        print(current_interviewer)
        current_interviewer_emp = Employee.query.filter_by(id=current_interviewer.employee_id).first()
        print(current_interviewer_emp)
        candidate_list[interview] = current_candidate
        interviewer_list[interview] = current_interviewer_emp
    return render_template('view_interview_list.html', candidates=candidate_list, interviewers=interviewer_list,
                           interviews=interviews)


@app.route('/interviewer/new', methods=['GET', 'POST'])
def create_new_interviewer():
    form = CreateNewInterviewerForm()
    if request.method == 'POST' and form.validate_on_submit():
        # save the interviewer to db
        interviewer = Interviewer()
        interviewer_emp = Employee()
        interviewer_emp.first_name = form.first_name.data
        interviewer_emp.last_name = form.last_name.data
        interviewer_emp.email = form.email.data
        interviewer_emp.contact_number = form.contact_number.data
        interviewer_emp.position = 'Employee'
        interviewer_emp.password = 'password'
        interviewer_emp.role = 'Interviewer'
        db.session.add(interviewer_emp)
        db.session.commit()
        interviewer.employee_id = interviewer_emp.id
        db.session.add(interviewer)
        db.session.commit()
        return redirect(url_for('view_all_interviews'))  # change this to view all interviewers.
    return render_template('create_new_interviewer.html', form=form)


@app.route('/position/new', methods=['GET', 'POST'])
def create_new_position():
    form = CreateNewPositionForm()
    if request.method == 'POST' and form.validate_on_submit():
        position = Position()
        position.title = form.title.data
        position.description = form.description.data
        db.session.add(position)
        db.session.commit()
        return redirect(url_for('view_all_positions'))
    return render_template('create_new_position.html', form=form)


@app.route('/position/all')
def view_all_positions():
    positions = Position.query.all()
    return render_template('view_position_list.html', positions=positions)


@app.route('/position/<position_id>')
def view_position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    return render_template('view_position.html', position=position)


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
    interviews = Interview.query.filter_by(candidate_id=candidate_id).order_by(Interview.round)
    cur_candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('interview_info.html', interviews=interviews, cur_candidate=cur_candidate)


@app.route('/manager_feedback/<int:candidate_id>', methods=['GET', 'POST'])
def manager_feedback(candidate_id):
    form = ManagerFeedbackForm()
    candidate = Candidate.query.get_or_404(candidate_id)
    if request.method == 'GET':
        return render_template('manager_feedback.html', candidate=candidate, form=form)
    if request.method == 'POST':
        if candidate.status == 'none':
            candidate.status = form.candidate_status.data
            db.session.add(candidate)
            db.session.commit()
            return redirect(url_for('final_selected_candidates'))

@app.route('/inprogress_candidates')
def inprogress_candidates():
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('inprogress_candidates.html', candidates=candidates)


# interviewer routes

@app.route("/")


# candidate routes

# candidate application link
@app.route('/application-form', methods=['GET', 'POST'])
def application():
    form = CandidateApplicationDetails()
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
