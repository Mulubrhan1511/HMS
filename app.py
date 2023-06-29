from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request, Blueprint, get_flashed_messages,g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import app, db, Patient, Doctor, Appointment, Reception, Laboratory, Report, Laboratory_test, Laboratory_type, Pharmacist, Medicine
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from datetime import date


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
            date_of_birth= '13/12/1996'
            gender = request.form['gender']
            city = request.form['city']
            state = request.form['state']
            flash('what about' + date_of_birth)
            new_user = Patient(name=name, email=email, password=hashed_password, state=state, city=city, date_of_birth=date_of_birth, gender=gender)
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
        elif user_type == 'pharmacist':
            specialty = request.form['specialty']
            phone = '0919151121'
            new_user = Pharmacist(name=name, password=hashed_password, specialty=specialty, phone=phone, email=email)
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
        pharmacist = Pharmacist.query.filter_by(email=email).first()
        if pharmacist and check_password_hash(pharmacist.password, password):
            # Log in the doctor
            login_user(pharmacist, remember=True)
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
    name = current_user if current_user.is_authenticated else ''
    patients = Patient.query.filter(Patient.doctor_id == current_user.id).all()
    # Render the doctor dashboard with a welcome message
    return render_template('doctor/doctor_dashboard.html', name = name, patients = patients)
@app.route('/pharmacist_dashboard')
@login_required
def pharmacist_dashboard():
# Get the current user's name

    # Render the doctor dashboard with a welcome message
    return render_template('pharmacist/pharmacist_dashboard.html')
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
        new_user = Patient(second_name=second_name,first_name=first_name, email=email, password=hashed_password, state=state, city=city, date_of_birth=date_of_birth, gender=gender, doctor_id=doctor_id)
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
        medicine_names = request.form.getlist('medicine_quantity[]')
        medicine_prices = request.form.getlist('medicine_price[]')
        medicine_totals = request.form.getlist('medicine_total[]')
        print(medicine_names)
        return render_template('doctor/medicine.html', patient=patient)
    patient = Patient.query.filter(Patient.id == patient_id).first()
    return render_template('doctor/medicine.html', patient=patient)
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
@app.route('/lab_payment', methods=['GET', 'POST'])
def lab_payment():
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.paid==0).all()
    return render_template('reception/payment.html', laboratory_test=laboratory_test)
@app.route('/payment_for_lab/<int:laboratory_test_id>', methods=['GET', 'POST'])
def payment_for_lab(laboratory_test_id):
    if request.method == 'POST':
        laboratory_test = Laboratory_test.query.filter(Laboratory_test.id == laboratory_test_id).first()
        laboratory_test.paid= 1
        db.session.commit()
        return redirect(url_for('lab_payment'))
    laboratory_test = Laboratory_test.query.filter(Laboratory_test.id==laboratory_test_id).first()
    return render_template('reception/detail_payment.html', laboratory_test=laboratory_test)
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
    app.run(debug=True)