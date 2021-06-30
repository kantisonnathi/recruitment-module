from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user

from app import app
from app.forms import LoginForm
from app.models import Employee


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('manager_candidates.html')
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee and employee.password == form.password.data:
            login_user(employee)
            return render_template('manager_candidates.html')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/interview/new')
def createNewCandidate():
    return render_template('manager_candidates.html')



