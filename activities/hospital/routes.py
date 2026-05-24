from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Patient, Doctor, Appointment, LabTest, Medicine
from datetime import datetime, date

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospital', template_folder='templates')

@hospital_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('hospital/dashboard.html', patients_count=Patient.query.filter_by(company_id=current_user.company_id).count(), doctors_count=Doctor.query.filter_by(company_id=current_user.company_id, status='active').count(), today_appointments=Appointment.query.filter_by(company_id=current_user.company_id, date=date.today()).count(), pending_appointments=Appointment.query.filter_by(company_id=current_user.company_id, status='scheduled').count(), recent_appointments=Appointment.query.filter_by(company_id=current_user.company_id).order_by(Appointment.date.desc()).limit(10).all())

@hospital_bp.route('/patients')
@login_required
def patients():
    patients_list = Patient.query.filter_by(company_id=current_user.company_id).order_by(Patient.id.desc()).all()
    return render_template('hospital/patients.html', patients=patients_list)

@hospital_bp.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    try:
        patient = Patient(company_id=current_user.company_id, name=request.form.get('name'), phone=request.form.get('phone'), email=request.form.get('email'), birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None, gender=request.form.get('gender'), address=request.form.get('address'), emergency_contact=request.form.get('emergency_contact'), blood_type=request.form.get('blood_type'), notes=request.form.get('notes'))
        db.session.add(patient); db.session.commit()
        flash('تم إضافة المريض بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.patients'))

@hospital_bp.route('/edit_patient/<int:id>', methods=['POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        patient.name = request.form.get('name'); patient.phone = request.form.get('phone')
        patient.email = request.form.get('email'); patient.gender = request.form.get('gender')
        patient.address = request.form.get('address'); patient.emergency_contact = request.form.get('emergency_contact')
        patient.blood_type = request.form.get('blood_type'); patient.notes = request.form.get('notes')
        patient.birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None
        db.session.commit(); flash('تم تحديث بيانات المريض بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.patients'))

@hospital_bp.route('/delete_patient/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(patient); db.session.commit()
        flash('تم حذف المريض بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.patients'))

@hospital_bp.route('/doctors')
@login_required
def doctors():
    doctors_list = Doctor.query.filter_by(company_id=current_user.company_id).all()
    return render_template('hospital/doctors.html', doctors=doctors_list)

@hospital_bp.route('/add_doctor', methods=['POST'])
@login_required
def add_doctor():
    try:
        doctor = Doctor(company_id=current_user.company_id, name=request.form.get('name'), specialty=request.form.get('specialty'), phone=request.form.get('phone'), email=request.form.get('email'), license_number=request.form.get('license_number'), status=request.form.get('status', 'active'))
        db.session.add(doctor); db.session.commit()
        flash('تم إضافة الطبيب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.doctors'))

@hospital_bp.route('/edit_doctor/<int:id>', methods=['POST'])
@login_required
def edit_doctor(id):
    doctor = Doctor.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        doctor.name = request.form.get('name'); doctor.specialty = request.form.get('specialty')
        doctor.phone = request.form.get('phone'); doctor.email = request.form.get('email')
        doctor.license_number = request.form.get('license_number'); doctor.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث بيانات الطبيب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.doctors'))

@hospital_bp.route('/delete_doctor/<int:id>', methods=['POST'])
@login_required
def delete_doctor(id):
    doctor = Doctor.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(doctor); db.session.commit()
        flash('تم حذف الطبيب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.doctors'))

@hospital_bp.route('/appointments')
@login_required
def appointments():
    appointments_list = Appointment.query.filter_by(company_id=current_user.company_id).order_by(Appointment.date.desc()).all()
    patients_list = Patient.query.filter_by(company_id=current_user.company_id).all()
    doctors_list = Doctor.query.filter_by(company_id=current_user.company_id).all()
    return render_template('hospital/appointments.html', appointments=appointments_list, patients=patients_list, doctors=doctors_list, now=date.today().strftime('%Y-%m-%d'))

@hospital_bp.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment():
    try:
        appt = Appointment(company_id=current_user.company_id, patient_id=request.form.get('patient_id') or None, doctor_id=request.form.get('doctor_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), time=request.form.get('time'), status=request.form.get('status', 'scheduled'), notes=request.form.get('notes'))
        db.session.add(appt); db.session.commit()
        flash('تم إضافة الموعد بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.appointments'))

@hospital_bp.route('/edit_appointment/<int:id>', methods=['POST'])
@login_required
def edit_appointment(id):
    appt = Appointment.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        appt.patient_id = request.form.get('patient_id') or None; appt.doctor_id = request.form.get('doctor_id') or None
        appt.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today()
        appt.time = request.form.get('time'); appt.status = request.form.get('status', 'scheduled')
        appt.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث الموعد بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.appointments'))

@hospital_bp.route('/delete_appointment/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appt = Appointment.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(appt); db.session.commit()
        flash('تم حذف الموعد بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.appointments'))

@hospital_bp.route('/medicines')
@login_required
def medicines():
    medicines_list = Medicine.query.filter_by(company_id=current_user.company_id).all()
    return render_template('hospital/medicines.html', medicines=medicines_list)

@hospital_bp.route('/add_medicine', methods=['POST'])
@login_required
def add_medicine():
    try:
        med = Medicine(company_id=current_user.company_id, name=request.form.get('name'), category=request.form.get('category'), price=float(request.form.get('price', 0)), quantity=float(request.form.get('quantity', 0)), expiry_date=datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None, status=request.form.get('status', 'active'))
        db.session.add(med); db.session.commit()
        flash('تم إضافة الدواء بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.medicines'))

@hospital_bp.route('/edit_medicine/<int:id>', methods=['POST'])
@login_required
def edit_medicine(id):
    med = Medicine.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        med.name = request.form.get('name'); med.category = request.form.get('category')
        med.price = float(request.form.get('price', 0)); med.quantity = float(request.form.get('quantity', 0))
        med.expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None
        med.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث الدواء بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.medicines'))

@hospital_bp.route('/delete_medicine/<int:id>', methods=['POST'])
@login_required
def delete_medicine(id):
    med = Medicine.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(med); db.session.commit()
        flash('تم حذف الدواء بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.medicines'))

@hospital_bp.route('/lab')
@login_required
def lab():
    tests = LabTest.query.filter_by(company_id=current_user.company_id).order_by(LabTest.date.desc()).all()
    patients_list = Patient.query.filter_by(company_id=current_user.company_id).all()
    return render_template('hospital/lab.html', tests=tests, patients=patients_list, now=date.today().strftime('%Y-%m-%d'))

@hospital_bp.route('/add_lab_test', methods=['POST'])
@login_required
def add_lab_test():
    try:
        test = LabTest(company_id=current_user.company_id, patient_id=request.form.get('patient_id') or None, test_name=request.form.get('test_name'), date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), result=request.form.get('result'), status=request.form.get('status', 'pending'))
        db.session.add(test); db.session.commit()
        flash('تم إضافة الفحص بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.lab'))

@hospital_bp.route('/edit_lab_test/<int:id>', methods=['POST'])
@login_required
def edit_lab_test(id):
    test = LabTest.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        test.patient_id = request.form.get('patient_id') or None; test.test_name = request.form.get('test_name')
        test.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today()
        test.result = request.form.get('result'); test.status = request.form.get('status', 'pending')
        db.session.commit(); flash('تم تحديث الفحص بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.lab'))

@hospital_bp.route('/delete_lab_test/<int:id>', methods=['POST'])
@login_required
def delete_lab_test(id):
    test = LabTest.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(test); db.session.commit()
        flash('تم حذف الفحص بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('hospital.lab'))
