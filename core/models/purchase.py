# core/models/purchase.py
from core import db
from datetime import datetime


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    invoice_number = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier = db.relationship('Supplier', backref='purchases')


class PurchaseItem(db.Model):
    __tablename__ = 'purchase_item'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)