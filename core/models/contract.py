# core/models/contract.py
from core import db
from datetime import datetime


class Contract(db.Model):
    __tablename__ = 'contract'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    contract_number = db.Column(db.String(50))
    type = db.Column(db.String(20), default='monthly')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)