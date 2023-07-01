from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
from flask_socketio import SocketIO, emit
from datetime import date, datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hospital_user:password@localhost/hospital_db'
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app, async_mode=None)

db = SQLAlchemy(app)
class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    type = db.Column(db.String(50))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    online = db.Column(db.Integer, server_default='0')
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    time = db.Column(db.Time)



class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
class Laboratory_test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    paid = db.Column(db.Integer)
    test = db.Column(db.Integer)
    price = db.Column(db.Integer)
class Laboratory_type(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
class Medicine(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    total = db.Column(db.Integer)
    price = db.Column(db.Integer)
    expired_date = db.Column(db.Date)
class Medication_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    paid = db.Column(db.Integer)
    test = db.Column(db.Integer)
    price = db.Column(db.Integer)