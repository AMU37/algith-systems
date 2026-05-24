# core/models/attendance.py
from core import db
from datetime import datetime


class DailyAttendance(db.Model):
    __tablename__ = 'daily_attendance'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='present')
    hours = db.Column(db.Float, default=0)
    daily_wage = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailyPayment(db.Model):
    __tablename__ = 'daily_payment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)