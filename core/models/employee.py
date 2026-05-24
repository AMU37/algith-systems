# core/models/employee.py
from core import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(50))
    code = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    position = db.Column(db.String(100))
    join_date = db.Column(db.Date, default=datetime.utcnow)
    wage_type = db.Column(db.String(20), default='monthly')
    comprehensive_salary = db.Column(db.Float, default=0)
    basic_salary = db.Column(db.Float, default=0)
    daily_wage = db.Column(db.Float, default=0)
    area = db.Column(db.String(100), default='غير محدد')
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)