from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hospital_user:password@localhost/hospital_db'
app.secret_key = 'your_secret_key_here'

db = SQLAlchemy(app)
class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    specialty = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))

class Laboratory(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    specialty = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

class Reception(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    specialty = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))