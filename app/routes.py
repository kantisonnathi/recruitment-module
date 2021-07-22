import datetime, flask_bcrypt
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm, InterviewForm, ManagerFeedbackForm, CreateNewEmployeeForm, CreateNewPositionForm
from app.models import Employee, Candidate, Interview, Interviewer, Application, Position, CandidateEducation, \
    CandidateProfession, CandidateCompensation

# candidate forms and validations imports
from app import db, bcrypt
from app.candidate_forms import CandidateRegistrationForm, CandidateLoginForm, CandidatePersonalDetails, \
    CandidateEducationDetails, CandidateCompensationDetails, CandidateProfessionDetails


# recruiter routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == "Manager":
            applications = Application.query.order_by(Application.id)
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('manager_candidates.html', applications=applications, candidates=candidates)
        else:
            candidates = Candidate.query.order_by(Candidate.id)
            return render_template('all_candidates.html', candidates=candidates)
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and employee.password == form.password.data:
            login_user(employee)
            if current_user.role == "Manager":
                applications = Application.query.order_by(Application.id)
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('manager_candidates.html', applications=applications, candidates=candidates)
            else:
                candidates = Candidate.query.order_by(Candidate.id)
                return render_template('all_candidates.html', candidates=candidates)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/application/<int:application_id>/interview/new', methods=['GET', 'POST'])
def create_new_interview(application_id):
    current_application = Application.query.filter_by(id=application_id).first()
    form = InterviewForm()
    candidate = Candidate.query.filter_by(id=current_application.candidate_id).first()
    interviewers = Employee.query.filter_by(role='Interviewer').all()
    job = Position.query.filter_by(id=current_application.position_id).first()
    if request.method == 'POST' and form.validate_on_submit():
        interview = Interview()
        interviewer_id = request.form.get('interviewer')
        interview.interviewer_id = interviewer_id
        interview.recruiter_id = current_user.id
        interview.application_id = application_id
        interview.duration = request.form.get('duration')
        interview.date = datetime.datetime.strptime(request.form.get('date'), "%d-%m-%Y").date()
        db.session.add(interview)
        db.session.commit()
        return redirect('/interview/' + str(interview.id) + '/set')
    return render_template('new_interview.html', title='Schedule Interview', form=form, interviewers=interviewers,
                           candidate=candidate, job=job)


@app.route('/application/all')
def view_all_applications():
    applications = Application.query.all()
    meta_cand = {}
    meta_pos = {}
    for appl in applications:
        curr_candidate = Candidate.query.filter_by(id=appl.candidate_id).first()
        curr_pos = Position.query.filter_by(id=appl.position_id).first()
        meta_cand[appl] = curr_candidate
        meta_pos[appl] = curr_pos
    return render_template('view_application_list.html', applications=applications, meta_cand=meta_cand,
                           meta_pos=meta_pos)


@app.route('/interview/<int:interview_id>/set', methods=['GET', 'POST'])
def set_interview_time(interview_id):
    current_interview = Interview.query.filter_by(id=interview_id).first()
    current_application = Application.query.filter_by(id=current_interview.application_id).first()
    current_candidate = Candidate.query.filter_by(id=current_application.candidate_id).first()
    job = Position.query.filter_by(id=current_application.position_id).first()
    interviewer = Interviewer.query.filter_by(id=current_interview.interviewer_id).first()
    interviews_by = Interview.query.filter_by(interviewer_id=interviewer.id).all()
    possible_start_times = time_population()
    for interview in interviews_by:
        curr_time = interview.start_time
        if curr_time in possible_start_times:
            possible_start_times.remove(curr_time)
    if request.method == 'POST':
        start_time = datetime.datetime.strptime(request.form.get('start_time'), "%H:%M:%S").time()
        current_interview.start_time = start_time
        end_time = datetime.time(start_time.hour + 1, start_time.minute, start_time.second)
        current_interview.end_time = end_time
        current_application.round += 1
        db.session.add(current_interview)
        db.session.add(current_application)
        db.session.commit()
        return redirect(url_for('view_interview', interview_id=current_interview.id))
    return render_template('set_time_interview.html', candidate=current_candidate, job=job, interviewer=interviewer,
                           times=possible_start_times)


@app.route('/interview/<interview_id>/delete')
def delete_interview(interview_id):
    curr_interview = Interview.query.filter_by(id=interview_id).first()
    curr_application = Application.query.filter_by(id=curr_interview.application_id).first()
    curr_application.round -= 1
    Interview.query.filter_by(id=interview_id).delete()
    db.session.add(curr_application)
    db.session.commit()
    return redirect(url_for('view_all_interviews'))


@app.route('/interview/<interview_id>', methods=['GET', 'POST'])
def view_interview(interview_id):
    curr_interview = Interview.query.filter_by(id=interview_id).first()
    interviewer = Interviewer.query.filter_by(id=curr_interview.interviewer_id).first()
    interviewer_emp = Employee.query.filter_by(id=interviewer.employee_id).first()
    current_application = Application.query.filter_by(id=curr_interview.application_id).first()
    candidate = Candidate.query.filter_by(id=current_application.candidate_id).first()
    job = Position.query.filter_by(id=current_application.position_id).first()
    return render_template('view_interview.html', position=job, candidate=candidate, interviewer=interviewer_emp,
                           interview=curr_interview, application=current_application)


@app.route('/interview/all')
def view_all_interviews():
    candidate_list = {}
    interviewer_list = {}
    interviews = Interview.query.all()
    for interview in interviews:
        current_application = Application.query.filter_by(id=interview.application_id).first()
        current_candidate = Candidate.query.filter_by(id=current_application.candidate_id).first()
        current_interviewer = Interviewer.query.filter_by(id=interview.interviewer_id).first()
        current_interviewer_emp = Employee.query.filter_by(id=current_interviewer.employee_id).first()
        candidate_list[interview] = current_candidate
        interviewer_list[interview] = current_interviewer_emp
    return render_template('view_interview_list.html', candidates=candidate_list, interviewers=interviewer_list,
                           interviews=interviews)


@app.route('/interviewer/new', methods=['GET', 'POST'])
def create_new_interviewer():
    form = CreateNewEmployeeForm()
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
        return redirect(url_for('view_all_interviewers'))
    return render_template('create_new_interviewer.html', form=form)


@app.route('/position/new', methods=['GET', 'POST'])
def create_new_position():
    form = CreateNewPositionForm()
    if request.method == 'POST' and form.validate_on_submit():
        position = Position()
        position.title = form.title.data
        position.description = form.description.data
        position.required_number = form.required_number.data
        position.number_applied = 0
        db.session.add(position)
        db.session.commit()
        flash('New position has been added!', 'info')
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


@app.route('/position/<position_id>/update', methods=['GET', 'POST'])
def update_position(position_id):
    position = Position.query.filter_by(id=position_id).first()
    form = CreateNewPositionForm()
    if request.method == 'GET':
        form.title.data = position.title
        form.description.data = position.description
        form.required_number.data = position.required_number
        return render_template('create_new_position.html', form=form)
    position.title = form.title.data
    position.description = form.description.data
    position.required_number = form.required_number.data
    db.session.add(position)
    db.session.commit()
    flash('New details have been saved!', 'info')
    return redirect(url_for('view_position', position_id=position.id))


@app.route('/interviewer/all')
def view_all_interviewers():
    interviewers = Interviewer.query.all()
    metadata = {}
    for interviewer in interviewers:
        emp = Employee.query.filter_by(id=interviewer.employee_id).first()
        metadata[interviewer] = emp
    return render_template('view_interviewer_list.html', interviewers=interviewers, metadata=metadata)


@app.route('/update', methods=['GET', 'POST'])
def update_info():  # PS: this works for all employees :)
    form = CreateNewEmployeeForm()
    if request.method == 'POST':
        changes = False
        if current_user.first_name != form.first_name.data:
            current_user.first_name = form.first_name.data
            changes = True
        if current_user.last_name != form.last_name.data:
            current_user.last_name = form.last_name.data
            changes = True
        if current_user.contact_number != form.contact_number.data:
            current_user.contact_number = form.contact_number.data
            changes = True
        if current_user.email != form.email.data:
            current_user.email = form.email.data
            changes = True
        if changes:
            flash('Your changes have been saved!', 'info')
            db.session.add(current_user)
            db.session.commit()
    else:
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.contact_number.data = current_user.contact_number
        form.email.data = current_user.email
    return render_template('update_self.html', form=form)


@app.route('/job/<int:job_id>/apply')
def create_application(job_id):
    role = current_user.role
    if role == 'Interviewer' or role == 'Recruiter' or role == 'Manager':
        flash('You cannot apply for a job', 'warning')
        return redirect(url_for('view_all_positions'))
    appl = Application(candidate_id=current_user.id, position_id=job_id, round=0, status='NULL')
    db.session.add(appl)
    db.session.commit()
    flash('You have applied for this job!', 'info')
    return redirect(url_for('view_all_positions'))


def time_population():
    list_times = []
    time = 9
    while True:
        list_times.append(datetime.time(time, 0, 0))
        list_times.append(datetime.time(time, 30, 0))
        time += 1
        if time == 13:
            time = 1
        if time == 6:
            break
    return list_times


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# manager routes

@app.route("/final_selected_candidates")
def final_selected_candidates():
    applications = Application.query.order_by(Application.id)
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('final_selected_candidates.html', applications=applications, candidates=candidates)


@app.route('/info/<int:candidate_id>')
def info(candidate_id):
    cur_candidate = Candidate.query.get_or_404(candidate_id)
    curr_candidate_education = CandidateEducation.query.get_or_404(candidate_id)
    curr_candidate_compensation = CandidateCompensation.query.get_or_404(candidate_id)
    curr_candidate_profession = CandidateProfession.query.get_or_404(candidate_id)
    return render_template('candidate_info.html', cur_candidate=cur_candidate,curr_candidate_education=curr_candidate_education,curr_candidate_compensation=curr_candidate_compensation,curr_candidate_profession=curr_candidate_profession)


@app.route('/candidate_interviews/<int:application_id>')
def candidate_interviews(application_id):
    cur_application = Application.query.get_or_404(application_id)
    interviews = Interview.query.filter_by(application_id=application_id).order_by(Interview.round)
    cur_candidate = Candidate.query.get_or_404(cur_application.candidate_id)
    return render_template('interview_info.html', interviews=interviews, cur_candidate=cur_candidate)


@app.route('/manager_feedback/<int:application_id>', methods=['GET', 'POST'])
def manager_feedback(application_id):
    form = ManagerFeedbackForm()
    cur_application = Application.query.get_or_404(application_id)
    candidate = Candidate.query.get_or_404(cur_application.candidate_id)
    if request.method == 'GET':
        return render_template('manager_feedback.html', cur_application=cur_application, candidate=candidate, form=form)
    if request.method == 'POST':
        if cur_application.status == 'none':
            cur_application.status = form.application_status.data
            cur_application.Feedback = form.feedback.data
            db.session.add(cur_application)
            db.session.commit()
            return redirect(url_for('final_selected_candidates'))
        else:
            return render_template('manager_feedback.html', cur_application=cur_application, candidate=candidate,
                                   form=form)


@app.route('/inprogress_candidates')
def inprogress_candidates():
    applications = Application.query.order_by(Application.id)
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('inprogress_candidates.html', candidates=candidates, applications=applications)


@app.route('/manager_view_all_positions')
def manager_view_all_positions():
    positions = Position.query.all()
    return render_template('manager_view_all_positions.html', positions=positions)


@app.route('/push_to_manager/<int:application_id>')
def push_to_manager(application_id):
    application = Application.query.get_or_404(application_id)
    application.push = True
    db.session.add(application)
    db.session.commit()
    return redirect(url_for('view_all_applications'))


@app.route('/manager_hold_applications')
def manager_hold_applications():
    applications = Application.query.order_by(Application.id)
    candidates = Candidate.query.order_by(Candidate.id)
    return render_template('manager_hold_applications.html', candidates=candidates, applications=applications)


# interviewer routes
@app.route('/interviewer_candidates_left', methods=['GET', 'POST'])
def interviewer_candidates_left():
    candidate = Candidate.query.get_or_404(Candidate.id)
    interviews = Interview.query.filter_by(is_done=False).filter_by(interviewer_id=current_user.id)
    emdict = {}
    for interview in interviews:
	    candidate = Candidate.query.filter_by(id=interview.candidate_id).first()
	    emdict[interview] = candidate
    return render_template('interviewer_candidates_left.html', emdict=emdict, interviews=interviews)

@app.route('/information/<int:candidate_id>', methods=['GET', 'POST'])
def information(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('information.html', candidate=candidate)

@app.route('/interviewer_candidate_feedback', methods=['GET', 'POST'])
def interviewer_candidate_feedback():
    interviews = Interview.query.filter_by(is_done=True).filter_by(interviewer_id=current_user.id).filter_by(feedback='')
    emdict = {}
    for interview in interviews:
	    candidate = Candidate.query.filter_by(id=interview.candidate_id).first()
	    emdict[interview] = candidate
    return render_template('interviewer_candidate_feedback.html', interviews=interviews, emdict=emdict)

@app.route('/interviewer_feedback/<int:candidate_id>', methods=['GET', 'POST'])
def interviewer_feedback(candidate_id):
    #skills = CandidateProfession.query.get_or_404(candidate_id)
    #skills = skills.split(",")
    #no_of_skills = skills.length()
    #forms = []
    #for skill in skills:
    #    forms.append(InterviewerFeedbackForm())
    #    db.session.add(Interviewer_Feedback(candidate_id = candidate_id, skill = skill))
    #    db.session.commit()
    form = InterviewerFeedbackForm()
    candidate = Candidate.query.get_or_404(candidate_id)
    interview = Interview.query.filter_by(candidate_id=candidate_id).first()
    #interviewer_feedback = []
    #for skill in skills:
    #    interviewer_feedback.append(Interviewer_Feedback.query.get_or_404(candidate_id))

    if request.method == 'GET':
        #return render_template('interviewer_feedback.html', candidate=candidate, forms=forms, form = form , skills = skills, no_of_skills = no_of_skills)
	return render_template('interviewer_feedback.html', candidate=candidate, form = form)
    if request.method == 'POST':
        if interview.feedback == '':
            candidate.status = form.interview_status.data
            interview.feedback = form.feedback.data
            #i = 0
            #for skill in skills:
            #    interviewer_feedback[i].feedback = forms[i].feedback.data
            #    db.session.add(interviewer_feedback[i])
            #    db.session.commit()
            #candidate.status = ''
            #interview.feedback = ''
    
            #candidate.status = ''
            #interview.feedback = ''
            db.session.add(candidate)
            db.session.add(interview)
            db.session.commit()
            return redirect(url_for('interviewer_candidate_done'))
        else:
            return redirect(url_for('interviewer_candidate_done'))

@app.route('/interviewer_candidate_done', methods=['GET', 'POST'])
def interviewer_candidate_done():
    interviews = Interview.query.filter_by(is_done=True).filter_by(interviewer_id=current_user.id)
    emdict = {}
    for interview in interviews:
        if (interview.feedback != ''):
	        candidate = Candidate.query.filter_by(id=interview.candidate_id).first()
	        emdict[interview] = candidate
    return render_template("interviewer_candidate_done.html", interviews=interviews, emdict=emdict)

# candidate routes

# candidate application form links

# candidate personal details link
@app.route('/apply/personal-details', methods=['GET', 'POST'])
def candidate_personal():
    form = CandidatePersonalDetails()
    if request.method == 'POST':
        candidate = Candidate.query.filter_by(email=form.email.data).first()
        candidate.first_name = form.firstname.data
        candidate.last_name = form.lastname.data
        candidate.contact_number = form.contact.data
        candidate.current_location = form.current_location.data
        candidate.pan_card = form.pancard.data
        # db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('candidate_education', candidate_id=candidate.id))
    return render_template('candidate_personal_details.html', title='personal_details', form=form)


# candidate education details link
@app.route('/apply/<candidate_id>/education-details', methods=['GET', 'POST'])
def candidate_education(candidate_id):
    form = CandidateEducationDetails()
    education = CandidateEducation()

    if request.method == 'POST' or form.validate_on_submit():
        education.candidate_id = candidate_id
        education.school_board = form.schoolboard.data
        education.school_percentage = form.schoolpercentage.data
        education.school_cgpa = form.schoolcgpa.data
        education.school_name = form.schoolname.data
        education.school_place = form.schoolplace.data
        education.intermediate_degree = form.intermediatedegree.data
        education.intermediate_completion = form.intermediatecompletion.data
        education.intermediate_percentage = form.intermediatepercentage.data
        education.intermediate_cgpa = form.intermediatecgpa.data
        education.intermediate_college = form.intermediatecollege.data
        education.intermediate_place = form.intermediateplace.data
        education.graduation_degree = form.graduationdegree.data
        education.graduation_completion = form.graduationcompletion.data
        education.graduation_percentage = form.graduationpercentage.data
        education.graduation_cgpa = form.graduationcgpa.data
        education.graduation_college = form.graduationcollege.data
        education.graduation_place = form.graduationplace.data
        education.postgraduation_degree = form.postgraduationdegree.data
        education.postgraduation_completion = form.postgraduationcompletion.data
        education.postgraduation_percentage = form.postgraduationpercentage.data
        education.postgraduation_cgpa = form.postgraduationcgpa.data
        education.postgraduation_college = form.postgraduationcollege.data
        education.postgraduation_place = form.postgraduationplace.data
        db.session.add(education)
        db.session.commit()
        return redirect(url_for('candidate_profession', candidate_id=candidate_id))
    return render_template('candidate_education_details.html', title='education_details', form=form)


# candidate profession details link
@app.route('/apply/<candidate_id>/profession-details', methods=['GET', 'POST'])
def candidate_profession(candidate_id):
    form = CandidateProfessionDetails()
    profession = CandidateProfession()

    if form.validate_on_submit():
        profession.candidate_id = candidate_id
        profession.current_designation = form.currentdesignation.data
        profession.years_of_experience = form.yearsofexperience.data
        profession.company_name = form.companyname.data
        profession.work_location = form.location.data
        profession.key_skill_sets = form.keyskillsets.data
        profession.linkedin_profile = form.linkedinprofile.data
        db.session.add(profession)
        db.session.commit()
        return redirect(url_for('candidate_compensation', candidate_id=candidate_id))
    return render_template('candidate_profession_details.html', title='profession_details', form=form)


# candidate compensation details
@app.route('/apply/<candidate_id>/compensation-details', methods=['GET', 'POST'])
def candidate_compensation(candidate_id):
    form = CandidateCompensationDetails()
    compensation = CandidateCompensation()

    if request.method == 'POST' or form.validate_on_submit():
        compensation.candidate_id = candidate_id
        compensation.current_ctc = form.currentctc.data
        compensation.expected_ctc = form.expectedctc.data
        compensation.notice_period = form.noticeperiod.data
        compensation.buyout_option = form.buyoutoption.data
        db.session.add(compensation)
        db.session.commit()
        return redirect(url_for('candidateHome'))
    return render_template('candidate_compensation_details.html', title='compensation_details', form=form)


# candidate home
@app.route('/candidate', methods=['GET', 'POST'])
def candidateHome():
    return render_template('candidate_home.html', title='candidateHome')


# candidate login link
@app.route('/candidate-login', methods=['GET', 'POST'])
def candidateLogin():
    form = CandidateLoginForm()
    if form.validate_on_submit():
        candidate = Candidate.query.filter_by(email=form.email.data).first()
        if candidate and bcrypt.check_password_hash(candidate.password, form.password.data):
            return redirect(url_for('candidateHome'))
        else:
            flash('Invalid Login credentials.Please try again!!', 'danger')
    return render_template('candidate_login.html', title='candidateLogin', form=form)


# candidate Registration link
@app.route('/candidate-registration', methods=['GET', 'POST'])
def candidateRegister():
    form = CandidateRegistrationForm()
    if form.validate_on_submit():
        hashed_password = flask_bcrypt.generate_password_hash(form.confirm_password.data).decode('utf-8')
        user = Candidate(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully! You are now able to login', 'success')
        return redirect(url_for('candidateLogin'))
    return render_template('candidate_registration.html', title='candidateRegister', form=form)
