# core/models/salary.py
from core import db
from datetime import datetime

class Salary(db.Model):
    __tablename__ = 'salary'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    basic_salary = db.Column(db.Float, default=0)
    additions_total = db.Column(db.Float, default=0)
    deductions_total = db.Column(db.Float, default=0)
    advances_deduction = db.Column(db.Float, default=0)
    net_salary = db.Column(db.Float, default=0)
    is_paid = db.Column(db.Boolean, default=False)
    paid_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)