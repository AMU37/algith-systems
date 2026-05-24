# core/models/client.py
from core import db
from datetime import datetime


class Client(db.Model):
    __tablename__ = 'client'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    balance = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ClientContract(db.Model):
    __tablename__ = 'client_contract'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    contract_number = db.Column(db.String(50))
    type = db.Column(db.String(20), default='monthly')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='contracts', lazy=True)