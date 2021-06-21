# an object of WSGI application
from flask import Flask,render_template,url_for
app = Flask(__name__) # Flask constructor

# A decorator used to tell the application
# which URL is associated function

candidates = [
    {
		'name': 'Ganesh',
		'mobile': '767849****',
		'email': 'ganesherddy2648@gmail.com',
		'SSC': 98
    },
    {
		'name': 'Robert',
		'mobile': '767849****',
		'email': 'ganesherddy2648@gmail.com',
		'SSC': 98
    },
	{
		'name': 'RajaBharat',
		'mobile': '767849****',
		'email': 'ganesherddy2648@gmail.com',
		'SSC': 98
    },
	{
		'name': 'Mark',
		'mobile': '767849****',
		'email': 'ganesherddy2648@gmail.com',
		'SSC': 98
    },

]

interviews = [
	{
		'candidate_name': 'Ganesh',
		'Interviewer_name': 'Bala',
		'feedback': 'Good',
		'selected': 'Yes'
	}
]

@app.route('/')
def hello():
	return render_template('manager_candidates.html',candidates=candidates)


@app.route('/info')
def info():
	return render_template('candidate_info.html',candidates=candidates)



@app.route('/interview')
def interview():
	return render_template('interview_info.html',interviews=interviews)


@app.route('/status')
def status():
	return render_template('final_selection.html',interviews=interviews)
