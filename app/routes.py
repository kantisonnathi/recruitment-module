import flask_bcrypt
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm, InterviewForm, ManagerFeedbackForm
from app.models import Employee, Candidate, Interview, Interviewer, CandidateEducation, CandidateProfession, CandidateCompensation

# candidate forms and validations imports
from app import db, bcrypt
from app.candidate_forms import CandidateRegistrationForm, CandidateLoginForm, CandidatePersonalDetails, CandidateEducationDetails, CandidateCompensationDetails, CandidateProfessionDetails



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
    interviews = Interview.query.filter_by(candidate_id=candidate_id).order_by(Interview.round)
    cur_candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('interview_info.html', interviews=interviews, cur_candidate=cur_candidate)


@app.route('/manager_feedback/<int:candidate_id>')
def manager_feedback(candidate_id):
    form = ManagerFeedbackForm()
    candidate = Candidate.query.get_or_404(candidate_id)
    return render_template('manager_feedback.html', candidate=candidate, form=form)


# candidate routes

# candidate application form links

# candidate personal details link
@app.route('/apply/personal-details', methods=['GET', 'POST'])
def candidate_personal():
    form = CandidatePersonalDetails()
    if request.method=='POST':
        candidate = Candidate.query.filter_by(email = form.email.data).first()
        candidate.first_name= form.firstname.data
        candidate.last_name= form.lastname.data
        candidate.contact_number= form.contact.data
        candidate.current_location= form.current_location.data
        candidate.pan_card = form.pancard.data
        #db.session.add(candidate)
        db.session.commit()
        return redirect(url_for('candidate_education',candidate_id=candidate.id))
    return render_template('candidate_personal_details.html', title='personal_details', form=form)


# candidate education details link
@app.route('/apply/<candidate_id>/education-details', methods=['GET','POST'])
def candidate_education(candidate_id):
    form = CandidateEducationDetails()
    education = CandidateEducation()

    if form.validate_on_submit():
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
        return redirect(url_for('candidate_profession', candidate_id = candidate_id))
    return render_template('candidate_education_details.html', title='education_details', form=form)


# candidate profession details link
@app.route('/apply/<candidate_id>/profession-details', methods=['GET','POST'])
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
        return redirect(url_for('candidate_compensation', candidate_id = candidate_id))
    return render_template('candidate_profession_details.html', title='profession_details', form=form)


# candidate compensation details
@app.route('/apply/<candidate_id>/compensation-details', methods=['GET','POST'])
def candidate_compensation(candidate_id):
    form = CandidateCompensationDetails()
    compensation = CandidateCompensation()

    if request.method=='POST' or form.validate_on_submit():
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
    return render_template('candidate_home.html', title = 'candidateHome')


# candidate login link
@app.route('/candidate-login', methods=['GET', 'POST'])
def candidateLogin():
    form = CandidateLoginForm()
    if form.validate_on_submit():
        candidate = Candidate.query.filter_by(email = form.email.data).first()
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
