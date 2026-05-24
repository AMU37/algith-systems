# core/models/service.py
from core import db
from datetime import datetime


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ServiceContract(db.Model):
    __tablename__ = 'service_contract'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    contract_number = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='service_contracts')


class ServiceOrder(db.Model):
    __tablename__ = 'service_order'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='service_orders')
    service = db.relationship('Service', backref='orders')