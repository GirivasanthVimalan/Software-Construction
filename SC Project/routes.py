from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, PatientRegistrationForm, AppointmentForm
from app.models import User, Patient, Doctor, Appointment

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    # Count stats for dashboard
    total_patients = Patient.query.count()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.scheduled_time) == db.func.date(db.func.now())
    ).count()
    
    return render_template('dashboard.html', 
                         total_patients=total_patients,
                         today_appointments=today_appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard'))
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route('/patients/register', methods=['GET', 'POST'])
@login_required
def register_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            insurance_provider=form.insurance_provider.data,
            insurance_policy_number=form.insurance_policy_number.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully!')
        return redirect(url_for('patient_profile', patient_id=patient.id))
    return render_template('patients/register.html', title='Register Patient', form=form)

@app.route('/patients/<int:patient_id>')
@login_required
def patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    appointments = patient.appointments.order_by(Appointment.scheduled_time.desc()).limit(5).all()
    records = patient.medical_records.order_by(MedicalRecord.record_date.desc()).limit(5).all()
    return render_template('patients/profile.html', patient=patient, 
                         appointments=appointments, records=records)

@app.route('/appointments/schedule', methods=['GET', 'POST'])
@login_required
def schedule_appointment():
    form = AppointmentForm()
    # Populate patient and doctor choices
    form.patient_id.choices = [(p.id, f"{p.first_name} {p.last_name}") 
                             for p in Patient.query.order_by(Patient.last_name).all()]
    form.doctor_id.choices = [(d.id, f"Dr. {d.user.username} ({d.specialization})") 
                            for d in Doctor.query.join(User).order_by(User.username).all()]
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            scheduled_time=form.scheduled_time.data,
            reason=form.reason.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment scheduled successfully!')
        return redirect(url_for('view_appointments'))
    
    return render_template('appointments/schedule.html', title='Schedule Appointment', form=form)

@app.route('/appointments')
@login_required
def view_appointments():
    page = request.args.get('page', 1, type=int)
    appointments = Appointment.query.order_by(
        Appointment.scheduled_time.desc()).paginate(
            page, app.config['APPOINTMENTS_PER_PAGE'], False)
    return render_template('appointments/list.html', 
                         title='Appointments',
                         appointments=appointments)