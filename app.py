from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint, get_flashed_messages,g, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Patient, Appointment, Report, Laboratory_test, Laboratory_type,  Medicine, Medication_report, User
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from datetime import date, datetime, timedelta
from flask_socketio import SocketIO, emit


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    user = None
    if user_id:
        user = Patient.query.get(int(user_id))
        if not user:
            user = User.query.get(int(user_id))
    return user
# Create the tables
with app.app_context():
    db.create_all()
socketio = SocketIO(app, async_mode='eventlet')

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        current_user.online = 1
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@socketio.on('disconnect')
def on_disconnect():
    if current_user.is_authenticated:
        current_user.online = 0
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        confirm_password = request.form['confirm_password']

        # Check if the two passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        # Check if the email is already registered
        new_user = User.query.filter_by(email=email).first()
        if new_user:
            flash('email address alreday exist', 'success')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password, method='sha256')
        date_of_birth= gender = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        type = request.form['type']
        new_user = User(second_name=second_name,first_name=first_name, email=email, password=hashed_password, state=state, city=city, date_of_birth=date_of_birth, gender=gender, type=type)
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
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Log in the patient
            login_user(user, remember=True)
            user.online = 1
            if user.type == 'doctor':
                flash('You have been logged in successfully.', 'success')
                return redirect(url_for('doctor_dashboard'))
            if user.type == 'reception':
                flash('You have been logged in successfully.', 'success')
                return redirect(url_for('reception_dashboard'))
            if user.type == 'laboratory':
                flash('You have been logged in successfully.', 'success')
                return redirect(url_for('laboratory_dashboard'))
            if user.type == 'pharmacist':
                flash('You have been logged in successfully.', 'success')
                return redirect(url_for('pharmacist_dashboard'))
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
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    return render_template('doctor/doctor_dashboard.html', name = name, patients = patients)
@app.route('/pharmacist_dashboard')
@login_required
def pharmacist_dashboard():
    # Get the current user's name
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    med = Medication_report.query.filter(Medication_report.paid == 1, Medication_report.test == 0).all()
    # Render the doctor dashboard with a welcome message
    return render_template('pharmacist/pharmacist_dashboard.html',med=med)
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
        date_of_birth= request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        new_user = Patient(second_name=second_name,first_name=first_name, email=email, password=hashed_password, state=state, city=city, date_of_birth=date_of_birth, gender=gender, doctor_id=doctor_id, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        # Redirect the user to the login page
        flash('You have created the patient', 'success')
        return redirect(url_for('reception_dashboard'))
        
    
    name = current_user if current_user.is_authenticated else ''
    #patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    doctors = User.query.filter(User.type == 'doctor').all()
    return render_template('reception/new_user.html', name=name, doctors = doctors)
@app.route('/reception_dashboard', methods=['GET', 'POST'])
@login_required
def reception_dashboard():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    cutoff = datetime.utcnow() - timedelta(minutes=1)
    online = User.query.filter(User.last_seen > cutoff).all()
    name = current_user if current_user.is_authenticated else ''
    doctors = User.query.filter(User.type == 'doctor').all()
    return render_template('reception/reception_dashboard.html', name=name, doctors = doctors, online=online)

@app.route('/laboratory_dashboard', methods=['GET', 'POST'])
@login_required
def laboratory_dashboard():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user.email if current_user.is_authenticated else ''
    laboratory_test =Laboratory_test.query.filter(Laboratory_test.paid==1, Laboratory_test.test==0).all()
    return render_template('laboratory/laboratory_dashboard.html', name=name, laboratory_test=laboratory_test)

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def patient_detail(patient_id):
    # Use the patient ID to look up the patient's details
    patients = Patient.query.filter(Patient.id == patient_id).first()
    patient = Patient.query.filter(Patient.id == patient_id).all()
    reports = Report.query.filter(Report.patient_id == patient_id).order_by(Report.date.desc()).all()
    # calculate the age of the patient
    dob = patients.date_of_birth
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    print("The age of the patient is:", age)
    return render_template('doctor/patient_detail.html', patient=patient, report=reports, age=age)
@app.route('/medicine/<int:patient_id>', methods=['GET', 'POST'])
def medicine(patient_id):
    if request.method == 'POST':
        patient = Patient.query.filter(Patient.id == patient_id).first()
        medicine_id = request.form.getlist('medicine_id[]')
        medicine_quantity = request.form.getlist('medicine_quantity[]')
        medicine_names = request.form.getlist('medicine_name[]')
        medicine_prices = request.form.getlist('medicine_price[]')
        medicine_totals = request.form.getlist('medicine_total[]')
        if not medicine_names:
            flash('Serche medicine and click to add', 'error')
            return redirect(url_for('medicine', patient_id=patient_id))

        if '' in medicine_quantity:
            flash('Please enter quantity for all medicines', 'error')
            return redirect(url_for('medicine', patient_id=patient_id))
        for i in range(len(medicine_id)):
            if int(medicine_totals[i]) < int(medicine_quantity[i]):
                message = 'Available ' + medicine_names[i] + ' is ' + medicine_totals[i] 
                flash(message, 'error')
                return redirect(url_for('medicine', patient_id=patient_id))
        dob = patient.date_of_birth
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        lab_report = "Medicine Report for Patient ID : {} Patient Name :{} Patient Gender : {} Patient Age : {} \n\nSelected Medicine Types:\n".format(patient_id,patient.first_name,patient.gender, age)
        total_price = 0
        for i in range(len(medicine_id)):
            one_price = int(medicine_prices[i]) * int(medicine_quantity[i])
            total_price = total_price + one_price
        lab_report += "- id           Name                Quaty\n\n\n"
        for i in range(len(medicine_id)):
            lab_report += "- {}         {}              {}\n\n\n".format(medicine_id[i],medicine_names[i],medicine_quantity[i])
        test = 0
        paid = 0
        p_report = Medication_report(data=lab_report, patient_id=patient_id, test=test, paid=paid, price=total_price)
        
        db.session.add(p_report)
        db.session.commit()
        for i in range(len(medicine_id)):
            medicine = Medicine.query.filter(Medicine.id == int(medicine_id[i])).first()
            medicine.total = int(medicine.total) - int(medicine_quantity[i])
            db.session.commit()
        flash(total_price, 'success')
        return redirect(url_for('medicine', patient_id=patient_id))
    report = Medication_report.query.filter(Medication_report.patient_id == patient_id).order_by(Medication_report.date.desc()).all()
    patient = Patient.query.filter(Patient.id == patient_id).first()
    return render_template('doctor/medicine.html', patient=patient, report=report)
@app.route('/laboratory_detail_doctor/<int:patient_id>', methods=['GET', 'POST'])
def laboratory_detail_doctor(patient_id):
    if request.method == 'POST':
        me = request.form.getlist('hello')
        price = 0
        for i in me:
            lab = Laboratory_type.query.filter(Laboratory_type.name == i).first()
            price = price + lab.price
        patients = Patient.query.filter(Patient.id == patient_id).first()
        dob = patients.date_of_birth
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        lab_report = "Lab Report for Patient ID : {} Patient Name :{} Patient Gender : {} Patient Age : {} \n\nSelected Lab Types:\n".format(patient_id,patients.first_name,patients.gender, age)
        for lab_type in me:
            lab_report += "- {}\n\n\n".format(lab_type)
        test = 0
        paid = 0
        p_report = Laboratory_test(data=lab_report, patient_id=patient_id, test=test, paid=paid, price=price)
        db.session.add(p_report)
        db.session.commit()
        return redirect(url_for('laboratory_detail_doctor', patient_id=patient_id))
    # Use the patient ID to look up the patient's details
    patients = Patient.query.filter(Patient.id == patient_id).first()
    patient = Patient.query.filter(Patient.id == patient_id).first()
    reports = Laboratory_test.query.filter(Laboratory_test.patient_id==patient_id).order_by(Laboratory_test.date.desc()).all()
    # calculate the age of the patient
    dob = patients.date_of_birth
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    laboratory_type = Laboratory_type.query.all()
    #print("The age of the patient is:", age)
    return render_template('doctor/laboratory_detail_doctor.html', patient=patient, report=reports, age=age, laboratory_type=laboratory_type)
@app.route('/laboratory_detail_lab/<int:laboratory_test_id>', methods=['GET', 'POST'])
def laboratory_detail_lab(laboratory_test_id):
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()

    return render_template('laboratory/laboratory_detail_lab.html', laboratory_test=laboratory_test)
@app.route('/med_detail/<int:med_id>', methods=['GET', 'POST'])
def med_detail(med_id):
    med_report = Medication_report.query.filter(Medication_report.id == med_id).first()

    return render_template('pharmacist/med_detail.html', med_report=med_report)
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
    current_user.online = 0
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
@app.route('/search_medicine', methods=['POST'])
def search_medicine():
    query = request.form.get('query')
    # perform a search for patients by name, email, or phone
    results = []
    if query:
        medicines = Medicine.query.filter(
            (Medicine.name.ilike(f'%{query}%')) |
            (Medicine.total.ilike(f'%{query}%')) |
            (Medicine.expired_date.ilike(f'%{query}%'))
        ).all()
        for medicines in medicines:
            results.append({'name': medicines.name, 'total': medicines.total, 'price': medicines.price, 'id': medicines.id})
    return jsonify(results)   

@app.route('/submit_report/<int:patient_id>', methods=['POST'])
def submit_report(patient_id):
    report_text = request.form['report']
    patient = Patient.query.get(patient_id)
    p_report = Report(data=report_text, patient_id=patient.id)
    db.session.add(p_report)
    db.session.commit()
    return redirect(url_for('patient_detail', patient_id=patient.id))
@app.route('/add_laboratory', methods=['GET', 'POST'])
def add_laboratory():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        new_lab = Laboratory_type(name=name, price=price)
        db.session.add(new_lab)
        db.session.commit()
        return redirect(url_for('add_laboratory'))
    return render_template('laboratory/add_laboratory.html')

@app.route('/add_medicine', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        total = request.form['total']
        expired_date = request.form['expired_date']
        new_med = Medicine(name=name, price=price, total=total, expired_date=expired_date)
        db.session.add(new_med)
        db.session.commit()
        return redirect(url_for('add_medicine'))
    return render_template('pharmacist/add_medicine.html')
@app.route('/submit_lab_report/<int:laboratory_test_id>', methods=['POST'])
def submit_lab_report(laboratory_test_id):
    report_data = request.form['report_data']
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()
    laboratory_test.data= report_data
    laboratory_test.test=1
    db.session.commit()
    return redirect(url_for('laboratory_dashboard'))
@app.route('/submit_med_report/<int:med_id>', methods=['POST'])
def submit_med_report(med_id):
    laboratory_test = Medication_report.query.filter(Medication_report.id == med_id).first()
    laboratory_test.test=1
    db.session.commit()
    return redirect(url_for('pharmacist_dashboard'))
@app.route('/lab_payment', methods=['GET', 'POST'])
def lab_payment():
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.paid==0).all()
    return render_template('reception/payment.html', laboratory_test=laboratory_test)
@app.route('/med_payment', methods=['GET', 'POST'])
def med_payment():
    med_report = Medication_report.query.filter(Medication_report.paid==0).all()
    return render_template('reception/medcine_payment.html', med_report=med_report)
@app.route('/payment_for_lab/<int:laboratory_test_id>', methods=['GET', 'POST'])
def payment_for_lab(laboratory_test_id):
    if request.method == 'POST':
        laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()
        laboratory_test.paid= 1
        db.session.commit()
        return redirect(url_for('lab_payment'))
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id==laboratory_test_id).first()
    return render_template('reception/detail_payment.html', laboratory_test=laboratory_test)
@app.route('/payment_for_med/<int:medication_report_id>', methods=['GET', 'POST'])
def payment_for_med(medication_report_id):
    if request.method == 'POST':
        med_test = Medication_report.query.filter(Medication_report.id == medication_report_id).first()
        med_test.paid= 1
        db.session.commit()
        return redirect(url_for('med_payment'))
    med_report = Medication_report.query.filter(Medication_report.id==medication_report_id).first()
    return render_template('reception/detail_med_payment.html', med_report=med_report)
@app.route('/edit_report', methods=['POST'])
def edit_report():
    report_id = request.form['report_id']
    report_data = request.form['report_data']
    report = Report.query.get(report_id)
    report.data = report_data
    db.session.commit()
    return jsonify(success=True)
@app.before_request
def before_request():
    g.messages = get_flashed_messages()


if __name__ == '__main__':
    socketio.run(app, debug=True)