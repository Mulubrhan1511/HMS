from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Patient, Doctor, Appointment, Reception, Laboratory, Report
from flask_login import login_user, login_required, logout_user, current_user, LoginManager


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    user = None
    if user_id:
        user = Patient.query.get(int(user_id))
        if not user:
            user = Doctor.query.get(int(user_id))
    return user
# Create the tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the two passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        # Check if the email is already registered
        patient = Patient.query.filter_by(email=email).first()
        doctor = Doctor.query.filter_by(email=email).first()
        reception = Reception.query.filter_by(email=email).first()
        laboratory = Laboratory.query.filter_by(email=email).first()
        if patient or doctor or reception or laboratory:
            flash('Email address already registered', 'error')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user in the database
        user_type = request.form['type']
        if user_type == 'patient':
            new_user = Patient(name=name, email=email, password=hashed_password)
        elif user_type == 'doctor':
            specialty = request.form['specialty']
            phone = '0919151121'
            new_user = Doctor(name=name, password=hashed_password, specialty=specialty, phone=phone, email=email)
        elif user_type == 'reception':
            specialty = request.form['specialty']
            phone = '0919151121'
            new_user = Reception(name=name, password=hashed_password, specialty=specialty, phone=phone, email=email)
        elif user_type == 'laboratory':
            specialty = request.form['specialty']
            phone = '0919151121'
            new_user = Laboratory(name=name, password=hashed_password, specialty=specialty, phone=phone, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Redirect the user to the login page
        flash('Your account has been created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    # Render the signup page
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password = request.form['password']

        # Check if the user is a patient
        patient = Patient.query.filter_by(email=email).first()
        if patient and check_password_hash(patient.password, password):
            # Log in the patient
            login_user(patient, remember=True)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('patient_dashboard'))

        # Check if the user is a doctor
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and check_password_hash(doctor.password, password):
            # Log in the doctor
            login_user(doctor, remember=True)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('doctor_dashboard'))
        reception = Reception.query.filter_by(email=email).first()
        if reception and check_password_hash(reception.password, password):
            # Log in the doctor
            login_user(reception, remember=True)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('reception_dashboard'))
        laboratory = Laboratory.query.filter_by(email=email).first()
        if laboratory and check_password_hash(laboratory.password, password):
            # Log in the doctor
            login_user(laboratory, remember=True)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('laboratory_dashboard'))
        # Invalid credentials
        flash('Invalid email or password', 'error')

    # Render the login page
    return render_template('login.html')

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
# Get the current user's name
    name = current_user if current_user.is_authenticated else ''
    # Render the patient dashboard with a welcome message
    return render_template('patient_dashboard.html', name=name)

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
# Get the current user's name
    name = current_user if current_user.is_authenticated else ''
    patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    return render_template('doctor/doctor_dashboard.html', name = name, patients = patients)
@app.route('/new_user', methods=['GET', 'POST'])
@login_required
def new_user():
# Get the current user's name
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        confirm_password = request.form['confirm_password']
        doctor_id = request.form.get('doctor')
        if not doctor_id:
            flash('Please select a doctor', 'error')
            return redirect(url_for('new_user'))
        # Check if the two passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('new_user'))
                # Check if the email is already registered
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            flash('Email address already registered', 'error')
            return redirect(url_for('new_user'))
        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = Patient(first_name=first_name, second_name=second_name,email=email, password=hashed_password, doctor_id=doctor_id, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        # Redirect the user to the login page
        flash('You have created the patient', 'success')
        return redirect(url_for('reception_dashboard'))
        
    
    name = current_user if current_user.is_authenticated else ''
    #patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    doctors = Doctor.query.filter().all()
    return render_template('reception/new_user.html', name=name, doctors = doctors)
@app.route('/reception_dashboard', methods=['GET', 'POST'])
@login_required
def reception_dashboard():
    name = current_user if current_user.is_authenticated else ''
    doctors = Doctor.query.filter().all()
    return render_template('reception/reception_dashboard.html', name=name, doctors = doctors)

@app.route('/laboratory_dashboard', methods=['GET', 'POST'])
@login_required
def laboratory_dashboard():
    name = current_user if current_user.is_authenticated else ''
    laboratory = Laboratory.query.filter().all()
    return render_template('laboratory/laboratory_dashboard.html', laboratory=laboratory, name=name)

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient_detail(patient_id):
    # Use the patient ID to look up the patient's details
    patient = Patient.query.filter(Patient.id == patient_id).all()
    # Render a template with the patient's details
    reports = Report.query.filter(Report.patient_id == patient_id).order_by(Report.date.desc()).all()
    return render_template('doctor/patient_detail.html', patient=patient, report=reports)
reception_bp = Blueprint('reception', __name__)
@reception_bp.route('/patient/<int:patient_id>')
def show_patient_detail(patient_id):
    # Retrieve the patient record from the database using the patient_id parameter
    patient = Patient.query.get(patient_id)

    # Render the patient detail template with the patient record
    return render_template('reception/patient_detail.html', patient=patient)
@app.route('/patient_detail_reception/<string:query>')
def patient_detail_reception(query):
    patient_detail = query.split()
    if len(patient_detail) < 3:
        flash('Incorrect user', 'error')
        return redirect(url_for('reception_dashboard'))
    patient = Patient.query.filter(Patient.email == patient_detail[1]).all()
    if patient:
        return render_template('reception/patient_detail.html', patient= patient)
    flash("Doesn't exist", 'error')
    return redirect(url_for('reception_dashboard'))
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # perform a search for patients by name, email, or phone
    results = []
    if query:
        patients = Patient.query.filter(
            (Patient.first_name.ilike(f'%{query}%')) |
            (Patient.email.ilike(f'%{query}%')) |
            (Patient.phone.ilike(f'%{query}%'))
        ).all()
        for patient in patients:
            results.append({'first_name': patient.first_name, 'second_name': patient.second_name,'email': patient.email, 'phone': patient.phone, 'id':patient.id})
    return jsonify(results)  

@app.route('/submit_report/<int:patient_id>', methods=['POST'])
def submit_report(patient_id):
    report_text = request.form['report']
    patient = Patient.query.get(patient_id)
    p_report = Report(data=report_text, patient_id=patient.id)
    db.session.add(p_report)
    db.session.commit()
    return redirect(url_for('patient_detail', patient_id=patient.id))

@app.route('/edit_report', methods=['POST'])
def edit_report():
    report_id = request.form['report_id']
    report_data = request.form['report_data']
    report = Report.query.get(report_id)
    report.data = report_data
    db.session.commit()
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(debug=True)