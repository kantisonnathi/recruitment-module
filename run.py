from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

candidates = [
    {
        'id': 1,
        'name': 'Ganesh',
        'mobile': '767849****',
        'email': 'ganesherddy2648@gmail.com',
        'SSC': 98
    },
    {
        'id': 2,
        'name': 'Robert',
        'mobile': '767849****',
        'email': 'ganesherddy2648@gmail.com',
        'SSC': 98
    },
    {
        'id': 3,
        'name': 'RajaBharat',
        'mobile': '767849****',
        'email': 'ganesherddy2648@gmail.com',
        'SSC': 98
    },
    {
        'id': 4,
        'name': 'Mark',
        'mobile': '767849****',
        'email': 'ganesherddy2648@gmail.com',
        'SSC': 98
    },

]

interviews = [
    {
        'candidate_name': 'Ganesh',
        'interviewer_name': 'Bala',
        'feedback': 'Good',
        'selected': 'Yes',
        'round': 3
    }
]

interviewers = [
    {
        'id': 1,
        'name': 'interviewer 1',
        'email': 'interviewer1@aizantit.com',
        'contact_number': '+91**********'
    },
    {
        'id': 2,
        'name': 'interviewer 2',
        'email': 'interviewer2@aizantit.com',
        'contact_number': '+91**********'
    }
]

recruiter = {
    'id': 1,
    'name': 'Jane Doe',
    'email': 'janedoe@aizantit.com',
    'contact_number': '+91********'
}


@app.route('/')
def hello():
    return render_template('manager_candidates.html', candidates=candidates)


@app.route('/info')
def info():
    return render_template('candidate_info.html', candidates=candidates)


@app.route('/interview')
def interview():
    return render_template('interview_info.html', interviews=interviews)


@app.route('/status')
def status():
    return render_template('final_selection.html', interviews=interviews)


@app.route('/recruiter/details')
def recruiterDetails():
    return render_template('recruiter_details.html', recruiter=recruiter)


@app.route('/scheduleInterview/<candidate_id_str>', methods=['GET', 'POST'])
def scheduleInterview(candidate_id_str):
    # if request.method == 'POST':
    candidate_id = int(candidate_id_str)
    candidate = getCandidateFromID(candidate_id) # query database for available interviewers instead of this method
    interview_form = ScheduleInterviewForm()
    if request.method == 'POST':
        interviewer_name = request.form.get('interviewer')
        interviews.append({
            'candidate_name': candidate['name'],
            'interviewer_name': interviewer_name
        })
    return render_template('schedule_interview.html', candidate=candidate, interviewers=interviewers, form=interview_form)


def getCandidateFromID(candidate_id):
    for candidate in candidates:
        if candidate['id'] == candidate_id:
            return candidate


class ScheduleInterviewForm(FlaskForm):
    interviewer = StringField('Interviewer name')
    submit = SubmitField('Submit')

