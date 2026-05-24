# core/models/sales.py
from core import db
from datetime import datetime


class SalesInvoice(db.Model):
    __tablename__ = 'sales_invoice'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    invoice_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='invoices')


class SalesInvoiceItem(db.Model):
    __tablename__ = 'sales_invoice_item'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)