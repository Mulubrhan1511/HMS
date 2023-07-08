from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint, get_flashed_messages,g, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Patient, Appointment, Report, Laboratory_test, Laboratory_type,  Medicine, Medication_report, User
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from datetime import date, datetime, timedelta
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename


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
    name = current_user if current_user.is_authenticated else ''
    return render_template('home.html',name=name)
@app.route('/health_information')
def health_information():
    name = current_user if current_user.is_authenticated else ''
    return render_template('Health_information.html',name=name)
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        confirm_password = request.form['confirm_password']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user_type = request.form['type']

        # Validate the form data
        if not first_name or not second_name or not email or not password or not confirm_password:
            flash('Please fill out all required fields', 'error')
            return redirect(url_for('login'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('login'))

        # Check if the email is already registered
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            name = current_user if current_user.is_authenticated else ''
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Save the uploaded image if present
        f = request.files['image']
        filename = secure_filename(f.filename)
        f.save('static/uploads/' + filename)
        # Create a new user object
        new_user = User(
            first_name=first_name,
            second_name=second_name,
            email=email,
            password=hashed_password,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            city=city,
            state=state,
            type=user_type,
            image=filename.encode('utf-8')
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully. Please log in.', 'success')
        name = current_user if current_user.is_authenticated else ''
        return redirect(url_for('login'))

    # Render the signup page
    return render_template('reg.html')

@app.route('/new_worker', methods=['GET', 'POST'])
def new_worker():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        confirm_password = request.form['confirm_password']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user_type = request.form['type']

        # Validate the form data
        if not first_name or not second_name or not email or not password or not confirm_password:
            flash('Please fill out all required fields', 'error')
            return redirect(url_for('new_worker'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('new_worker'))

        # Check if the email is already registered
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists', 'error')
            name = current_user if current_user.is_authenticated else ''
            return redirect(url_for('new_worker'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Save the uploaded image if present
        f = request.files['image']
        filename = secure_filename(f.filename)
        f.save('static/uploads/' + filename)
        # Create a new user object
        new_user = User(
            first_name=first_name,
            second_name=second_name,
            email=email,
            password=hashed_password,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            city=city,
            state=state,
            type=user_type,
            image=filename.encode('utf-8')
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created successfully. Please log in.', 'success')
        name = current_user if current_user.is_authenticated else ''
        return redirect(url_for('admin_dashboard'))

    # Render the signup page
    return render_template('admin/new_worker.html',name=name)

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
            if user.type == 'admin':
                flash('You have been logged in successfully.', 'success')
                return redirect(url_for('admin_dashboard'))
        patient = Patient.query.filter_by(email=email).first()
        if patient and check_password_hash(patient.password, password):
            login_user(patient, remember=True)
            flash('You have been logged in successfully.', 'success')
            return redirect(url_for('patient_dashboard'))
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))
    # Render the login page
    return render_template('login.html')

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
# Get the current user's name
    name = current_user if current_user.is_authenticated else ''
    # Render the patient dashboard with a welcome message
    return render_template('home.html', name=name)

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    # Get the current user's name
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    ages = []
    for patient in patients:
        dob = patient.date_of_birth
        age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
        ages.append(age)
    # Render the doctor dashboard with a welcome message
    return render_template('doctor/doctor_dashboard.html', name = name, patients = patients,ages=ages)
@app.route('/pharmacist_dashboard')
@login_required
def pharmacist_dashboard():
    # Get the current user's name
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    med = Medication_report.query.filter(Medication_report.paid == 1, Medication_report.test == 0).all()
    name = current_user if current_user.is_authenticated else ''
    # Render the doctor dashboard with a welcome message
    return render_template('pharmacist/pharmacist_dashboard.html',med=med,name=name)
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # Get the current user's name
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    doctor_count = User.query.filter_by(type='doctor').count()
    laboratory_count = User.query.filter_by(type='laboratory').count()
    reception_count = User.query.filter_by(type='reception').count()
    pharmacist_count = User.query.filter_by(type='pharmacist').count()
    laboratory_type_count = Laboratory_type.query.filter_by().count()
    medicine_count = Medicine.query.filter_by().count()
    laboratory_test = Laboratory_test.query.filter_by().count()
    medication_report = Medication_report.query.filter_by().count()
    # Render the doctor dashboard with a welcome message
    return render_template('admin/admin_dashboard.html', name=name,doctor_count=doctor_count, laboratory_count=laboratory_count, reception_count=reception_count, pharmacist_count=pharmacist_count, laboratory_type_count=laboratory_type_count,medicine_count=medicine_count, laboratory_test=laboratory_test,medication_report=medication_report)
@app.route('/detail_user/<string:type>', methods=['GET', 'POST'])
@login_required
def detail_user(type):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    # Use the patient ID to look up the patient's details
    type = type.capitalize()
    user = User.query.filter_by(type=type).all()
    cutoff = datetime.utcnow() - timedelta(minutes=1)
    online = User.query.filter(User.last_seen > cutoff).all()
    online_id = [user.id for user in online]
    return render_template('admin/user_detail.html', user=user,name=name,type=type,online_id=online_id,online=online)
@app.route('/new_user', methods=['GET', 'POST'])
@login_required
def new_user():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered', 'error')
            return redirect(url_for('signup'))
        if not doctor_id:
            flash('Please select a doctor', 'error')
            return redirect(url_for('signup'))
        # Check if the two passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
                # Check if the email is already registered
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            flash('Email address already registered', 'error')
            return redirect(url_for('signup'))
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
        flash('You have created an acount', 'success')
        return redirect(url_for('login'))
    #patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    doctors = User.query.filter(User.type == 'doctor').all()
    return render_template('signup.html',doctors=doctors)
@app.route('/reception_dashboard', methods=['GET', 'POST'])
@login_required
def reception_dashboard():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    cutoff = datetime.utcnow() - timedelta(minutes=1)
    online = User.query.filter(User.last_seen > cutoff).all()
    name = current_user if current_user.is_authenticated else ''
    doctors = User.query.filter(User.type == 'doctor',User.last_seen > cutoff).all()
    return render_template('reception/reception_dashboard.html', name=name, doctors = doctors, online=online)
@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        doctor_id = request.form.get('doctor')
        date_str = request.form['date']
        time_str = request.form['time']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        new_appoitment = Appointment(patient_id=name.id,doctor_id=doctor_id,time=time,date=date)
        db.session.add(new_appoitment)
        db.session.commit()
        flash('Appointment Made', 'success')
        return redirect(url_for('patient_dashboard'))
    cutoff = datetime.utcnow() - timedelta(minutes=1)
    doctors = User.query.filter(User.type == 'doctor',User.last_seen > cutoff).all()
    return render_template('appointments.html', doctors=doctors,name=name)

@app.route('/laboratory_dashboard', methods=['GET', 'POST'])
@login_required
def laboratory_dashboard():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    laboratory_test =Laboratory_test.query.filter(Laboratory_test.paid==1, Laboratory_test.test==0).all()
    return render_template('laboratory/laboratory_dashboard.html', name=name, laboratory_test=laboratory_test)

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def patient_detail(patient_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    # Use the patient ID to look up the patient's details
    patient = Patient.query.filter(Patient.id == patient_id).first()
    reports = Report.query.filter(Report.patient_id == patient_id).order_by(Report.date.desc()).all()
    # calculate the age of the patient
    dob = patient.date_of_birth
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    return render_template('doctor/patient_detail.html', patient=patient, report=reports, age=age,name=name)
@app.route('/appointment_doctor', methods=['GET', 'POST'])
@login_required
def appointment_doctor():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    # Use the patient ID to look up the patient's details
    patient = Patient.query.filter().all()
    appointments = Appointment.query.filter(Appointment.doctor_id == name.id).all()
    return render_template('doctor/appoitment.html',appointments=appointments,name=name,patient=patient)
@app.route('/medicine/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def medicine(patient_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
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
    return render_template('doctor/medicine.html', patient=patient, report=report,name=name)
@app.route('/laboratory_detail_doctor/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def laboratory_detail_doctor(patient_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
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
    laboratory_type = Laboratory_type.query.filter(Laboratory_type.active==1).all()
    #print("The age of the patient is:", age)
    return render_template('doctor/laboratory_detail_doctor.html', patient=patient, report=reports, age=age, laboratory_type=laboratory_type,name=name)
@app.route('/laboratory_detail_lab/<int:laboratory_test_id>', methods=['GET', 'POST'])
@login_required
def laboratory_detail_lab(laboratory_test_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()

    return render_template('laboratory/laboratory_detail_lab.html', laboratory_test=laboratory_test,name=name)
@app.route('/med_detail/<int:med_id>', methods=['GET', 'POST'])
@login_required
def med_detail(med_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    med_report = Medication_report.query.filter(Medication_report.id == med_id).first()

    return render_template('pharmacist/med_detail.html', med_report=med_report,name=name)
reception_bp = Blueprint('reception', __name__)
@reception_bp.route('/patient/<int:patient_id>')
@login_required
def show_patient_detail(patient_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    # Retrieve the patient record from the database using the patient_id parameter
    patient = Patient.query.get(patient_id)

    # Render the patient detail template with the patient record
    return render_template('reception/patient_detail.html', patient=patient,name=name)
@app.route('/patient_detail_reception/<string:query>')
@login_required
def patient_detail_reception(query):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    patient_detail = query.split()
    if len(patient_detail) < 3:
        flash('Incorrect user', 'error')
        return redirect(url_for('reception_dashboard'))
    patient = Patient.query.filter(Patient.email == patient_detail[1]).first()
    if patient:
        cutoff = datetime.utcnow() - timedelta(minutes=1)
        doctors = User.query.filter(User.type == 'doctor',User.last_seen > cutoff).all()
        return render_template('reception/patient_detail.html', patient= patient,name=name,doctors=doctors)
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
@login_required
def add_laboratory():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        new_lab = Laboratory_type(name=name, price=price)
        db.session.add(new_lab)
        db.session.commit()
        return redirect(url_for('add_laboratory'))
    return render_template('laboratory/add_laboratory.html',name=name)

@app.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def add_medicine():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        total = request.form['total']
        expired_date = request.form['expired_date']
        new_med = Medicine(name=name, price=price, total=total, expired_date=expired_date)
        db.session.add(new_med)
        db.session.commit()
        return redirect(url_for('add_medicine'))
    return render_template('pharmacist/add_medicine.html',name=name)
@app.route('/submit_lab_report/<int:laboratory_test_id>', methods=['POST'])
@login_required
def submit_lab_report(laboratory_test_id):
    report_data = request.form['report_data']
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()
    laboratory_test.data= report_data
    laboratory_test.test=1
    db.session.commit()
    return redirect(url_for('laboratory_dashboard'))
@app.route('/laboratory_test', methods=['GET'])
@login_required
def laboratory_test():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    laboratory_type = Laboratory_type.query.filter().all()
    return render_template('laboratory/laboratory_type.html', name=name,laboratory_type=laboratory_type)
@app.route('/submit_med_report/<int:med_id>', methods=['POST'])
@login_required
def submit_med_report(med_id):
    laboratory_test = Medication_report.query.filter(Medication_report.id == med_id).first()
    laboratory_test.test=1
    db.session.commit()
    return redirect(url_for('pharmacist_dashboard'))
@app.route('/lab_payment', methods=['GET', 'POST'])
@login_required
def lab_payment():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.paid==0).all()
    return render_template('reception/payment.html', laboratory_test=laboratory_test,name=name)
@app.route('/med_payment', methods=['GET', 'POST'])
@login_required
def med_payment():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    med_report = Medication_report.query.filter(Medication_report.paid==0).all()
    return render_template('reception/medcine_payment.html', med_report=med_report,name=name)
@app.route('/payment_for_lab/<int:laboratory_test_id>', methods=['GET', 'POST'])
@login_required
def payment_for_lab(laboratory_test_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()
        laboratory_test.paid= 1
        db.session.commit()
        return redirect(url_for('lab_payment'))
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id==laboratory_test_id).first()
    return render_template('reception/detail_payment.html', laboratory_test=laboratory_test,name=name)
@app.route('/payment_for_med/<int:medication_report_id>', methods=['GET', 'POST'])
@login_required
def payment_for_med(medication_report_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        med_test = Medication_report.query.filter(Medication_report.id == medication_report_id).first()
        med_test.paid= 1
        db.session.commit()
        return redirect(url_for('med_payment'))
    med_report = Medication_report.query.filter(Medication_report.id==medication_report_id).first()
    return render_template('reception/detail_med_payment.html', med_report=med_report,name=name)
@app.route('/edit_report', methods=['POST'])
def edit_report():
    report_id = request.form['report_id']
    report_data = request.form['report_data']
    report = Report.query.get(report_id)
    report.data = report_data
    db.session.commit()
    return jsonify(success=True)
@app.route('/assign_doctor/<int:patient_id>', methods=['POST'])
def assign_doctor(patient_id):
    doctor_id = request.form['doctor']
    patient = Patient.query.filter(Patient.id == patient_id).first()
    patient.doctor_id = doctor_id
    db.session.commit()
    return redirect(url_for('reception_dashboard'))
@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    patients = Patient.query.filter_by(doctor_id=user_id).all()
    for patient in patients:
        patient.doctor_id = None
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
@app.route('/detail_laboratory_type', methods=['GET', 'POST'])
@login_required
def detail_laboratory_type():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    lab_type = Laboratory_type.query.filter().all()
    return render_template('admin/detail_laboratory_type.html', lab_type=lab_type,name=name)
@app.route('/detail_medicine', methods=['GET', 'POST'])
@login_required
def detail_medicine():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    medicine = Medicine.query.filter().all()
    return render_template('admin/detail_medicine.html', medicine=medicine,name=name)

@app.route('/detail_laboratory_test', methods=['GET', 'POST'])
@login_required
def detail_laboratory_test():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    laboratory_test = Laboratory_test.query.filter().all()
    return render_template('admin/detail_laboratory_test.html',laboratory_test=laboratory_test,name=name)

@app.route('/detail_orderd_medicin', methods=['GET', 'POST'])
@login_required
def detail_orderd_medicin():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    medication_report = Medication_report.query.filter().all()
    return render_template('admin/detail_orderd_medicin.html',medication_report=medication_report,name=name)
@app.route('/edit_lab_type/<int:laboratory_type_id>', methods=['GET', 'POST'])
def edit_lab_type(laboratory_type_id):
    # Retrieve the id and active state of the laboratory type from the request data
    # Update the laboratory type in your data model (e.g., database)
    # Here's an example using SQLAlchemy:
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        active_status = request.form['active']
        name = request.form['name']
        price = request.form['price']
        laboratory_type = Laboratory_type.query.filter(Laboratory_type.id==laboratory_type_id).first()
        laboratory_type.name =name
        laboratory_type.price=price
        if active_status == "True":
            laboratory_type.active=True
        else:
            laboratory_type.active=False
        db.session.commit()
        return redirect(url_for('laboratory_test'))
    laboratory_type = Laboratory_type.query.filter(Laboratory_type.id==laboratory_type_id).first()
    return render_template('laboratory/edit_lab_type.html',laboratory_type=laboratory_type,name=name)
@app.route('/edit_profile_admin/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(user_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user = User.query.get(user_id)
        user.first_name=first_name
        user.second_name=second_name
        user.email=email
        user.date_of_birth=date_of_birth
        user.gender=gender
        user.city=city
        user.state=state
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_profile.html',name=name)
@app.route('/edit_profile_doctor/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile_doctor(user_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user = User.query.get(user_id)
        user.first_name=first_name
        user.second_name=second_name
        user.email=email
        user.date_of_birth=date_of_birth
        user.gender=gender
        user.city=city
        user.state=state
        db.session.commit()
        return redirect(url_for('doctor_dashboard'))
    return render_template('doctor/edit_profile.html',name=name)
@app.route('/edit_profile_laboratory/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile_laboratory(user_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user = User.query.get(user_id)
        user.first_name=first_name
        user.second_name=second_name
        user.email=email
        user.date_of_birth=date_of_birth
        user.gender=gender
        user.city=city
        user.state=state
        db.session.commit()
        return redirect(url_for('laboratory_dashboard'))
    return render_template('laboratory/edit_profile.html',name=name)
@app.route('/edit_profile_pharmacist/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile_pharmacist(user_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user = User.query.get(user_id)
        user.first_name=first_name
        user.second_name=second_name
        user.email=email
        user.date_of_birth=date_of_birth
        user.gender=gender
        user.city=city
        user.state=state
        db.session.commit()
        return redirect(url_for('pharmacist_dashboard'))
    return render_template('pharmacist/edit_profile.html',name=name)
@app.route('/edit_profile_reception/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile_reception(user_id):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    name = current_user if current_user.is_authenticated else ''
    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        email = request.form['email']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        city = request.form['city']
        state = request.form['state']
        user = User.query.get(user_id)
        user.first_name=first_name
        user.second_name=second_name
        user.email=email
        user.date_of_birth=date_of_birth
        user.gender=gender
        user.city=city
        user.state=state
        db.session.commit()
        return redirect(url_for('reception_dashboard'))
    return render_template('reception/edit_profile.html',name=name)
@app.before_request
def before_request():
    g.messages = get_flashed_messages()


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
