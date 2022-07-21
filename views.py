"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from flask_login import login_required, LoginManager
from app.forms import patientSignUpForm, doctorSignUpForm, patientLoginForm, doctorLoginForm, makeAppointment
from app.models import DoctorsProfile, PatientsProfile, Appointment, AppointmentSchedule, PatientRecord
from flask_wtf.csrf import generate_csrf
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html', title ='Home')


@app.route('/about/')
def about(): 
    """Render the website's about page."""
    return render_template('about.html', title ='About')

@app.route('/patientSignUp', methods=["GET","POST"])
def patientSignUp():
    form = patientSignUpForm()
    if form.validate_on_submit():
        patient_info = PatientsProfile(first_name=form.first_name.data, last_name=form.last_name.data, 
        DOB=form.DOB.data, emailAddress=form.emailAddress.data, username=form.username.data)
        patient_info.set_password(form.password.data)
        db.session.add(patient_info)
        db.session.commit()
        return 'success'
    return render_template('patientSignUp.html', form=form)

@app.route('/doctorSignUp', methods=["GET", 'POST'])
def doctorSignUp():
    form = doctorSignUpForm()
    if  form.validate_on_submit():
        doctor_info = DoctorsProfile(first_name = form.first_name.data, last_name = form.last_name.data, specialty = form.specialty.data,
        title = form.title.data, phoneNumber = form.phoneNumber.data, emailAddress = form.emailAddress.data, companyName = form.companyName.data)
        doctor_info.set_password(form.password.data)
        doctor = DoctorsProfile.query.filter_by(emailAddress=emailAddress).sixth()
        db.session.add(doctor_info)
        db.session.commit()
        return 'success'
    return render_template('doctorSignUp.html', form=form) 

@app.route("/doctorlogin", methods=["GET", "POST"])
def doclogin():
    form = doctorLoginForm()
    if  form.validate_on_submit() and request.method =='POST':
        emailAddress = form.emailAddress.data
        password = form.password.data
        doctor = DoctorsProfile.query.filter_by(emailAddress = emailAddress).first()
        print (doctor.password)
        if doctor is not None and check_password_hash(doctor.password, password):
            login_user(doctor)
            flash("You have been logged in!", 'success')
        else:
            flash("Credentials does not match", 'danger')
    return render_template('doclogin.html', form=form)

@app.route("/patientlogin", methods=["GET", "POST"])
def patientlogin():
    form = patientLoginForm()
    if  form.validate_on_submit() and request.method =='POST':
        username = form.username.data
        emailAddress = form.emailAddress.data
        password = form.password.data
        patient = PatientsProfile.query.filter_by(username = username).first()
        if patient is not None and check_password_hash(patient.password, password):
            login_user(patient)
            flash("You have been logged in!", 'success')
        else:
            flash("Credentials does not match", 'danger')
    return render_template('patientlogin.html', form=form)

@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    form = makeAppointment()
    if request.method == "GET":
        first_name = form.first_name.data
    return render_template('appointments.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", 'success')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(patientId):
    return PatientsProfile.query.get(int(patientId))

@login_manager.user_loader
def load_user(doctorId):
    return DoctorsProfile.query.get(int(doctorId))
###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
