# core/models/invoice.py
from core import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoice'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    invoice_number = db.Column(db.String(50))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)