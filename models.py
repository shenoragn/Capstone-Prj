import email
from pydoc import doc
from . import db
from werkzeug.security import generate_password_hash


class DoctorsProfile(db.Model):
    __tablename__ = 'doctor_profiles'

    doctorId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    specialty = db.Column(db.String(80))
    title = db.Column(db.String(80))
    phoneNumber = db.Column(db.String(80))
    emailAddress = db.Column(db.String(160))
    companyName  = db.Column(db.String(80))
    password = db.Column(db.String(255), unique=True)

    def __init__(self, doctorId,first_name, last_name, specialty,
    title, phoneNumber, emailAddress, companyName, password):
        self.doctorId = doctorId
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.title = title
        self.phoneNumber = phoneNumber
        self.emailAddress = emailAddress
        self.companyName = companyName
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

class PatientsProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of PatientsProfile would create a
    # patient_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'patient_profiles'

    patientId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    DOB = db.Column(db.DateTime)
    emailAddress = db.Column(db.String(160))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, patientId, first_name, last_name, DOB, emailAddress, username, password):
        self.patientId = patientId
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.emailAddress = emailAddress
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    patientId = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(160))
    last_name = db.Column(db.String(80))
    emailAddress = db.Column(db.String(160))
    phoneNumber = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    doctor = db.Column(db.String(80))
    reason = db.Column(db.String(255))
    link = db.Column(db.String(255))

    def __init__(self, patientId, first_name, last_name, emailAddress, phoneNumber, date, doctor, reason, link):
        self.patientId = patientId
        self.first_name = first_name
        self.last_name = last_name
        self.emailAddress = emailAddress
        self.phoneNumber = phoneNumber
        self.date = date
        self.doctor = doctor
        self.reason = reason
        self.link = link

class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    doctorId = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(160))
    time = db.Column(db.String(60))
    date = db.Column(db.DateTime)

    def __init__(self, doctorId, doctor_name, time, date, emailAddress):
        self.doctorId = doctorId 
        self.doctor_name = doctor_name
        self.time = time
        self.date = date
        self.emailAddress = emailAddress

class PatientRecord(db.Model):
    __tablename__ = 'patient_record'
    patientId = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(160))
    patient_illness = db.Column(db.String(160))
    patient_report = db.Column(db.String(255))
    medication = db.Column(db.String(255))
    phoneNumber = db.Column(db.String(255))

    def __init__(self, patientID, patientname, patient_illness, patient_report, medication, phoneNumber):
        self.patientId = patientID
        self.patient_name = patientname
        self.patient_illness = patient_illness
        self.patient_report = patient_report
        self.medication = medication
        self.phoneNumber = phoneNumber

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_patientId(self):
        try:
            return str(self.patientId)  # python 2 support
        except NameError:
            return str(self.patientId)  # python 3 support

    def get_doctorId(self):
        try:
            return str(self.doctorId)  # python 2 support
        except NameError:
            return str(self.doctorId)  # python 3 support

    def __repr__(self):
        return '<PatientsProfile %r>' % (self.username)

    def __repr__(self):
        return '<DoctorsProfile %r>' % (self.emailAddress)

