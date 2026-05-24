# core/models/hospital.py
from core import db
from datetime import datetime


class Patient(db.Model):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(120))
    blood_type = db.Column(db.String(5))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Doctor(db.Model):
    __tablename__ = 'doctor'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    license_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')


class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    time = db.Column(db.String(10))
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)


class LabTest(db.Model):
    __tablename__ = 'lab_test'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    test_name = db.Column(db.String(120))
    date = db.Column(db.Date, default=datetime.utcnow)
    result = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')


class Medicine(db.Model):
    __tablename__ = 'medicine'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Float, default=0)
    expiry_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')