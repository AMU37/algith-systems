# core/models/deduction.py
from core import db
from datetime import datetime

class Deduction(db.Model):
    __tablename__ = 'deduction'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    reason = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    month = db.Column(db.String(7))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Addition(db.Model):
    __tablename__ = 'addition'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    reason = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    month = db.Column(db.String(7))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Advance(db.Model):
    __tablename__ = 'advance'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    amount = db.Column(db.Float, default=0)
    remaining = db.Column(db.Float, default=0)
    monthly_deduction = db.Column(db.Float, default=0)
    date = db.Column(db.Date, default=datetime.utcnow)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)