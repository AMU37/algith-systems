# core/models/product.py
from core import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    type = db.Column(db.String(20), default='product')
    unit = db.Column(db.String(20))
    purchase_price = db.Column(db.Float, default=0)
    sale_price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Float, default=0)
    min_quantity = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)