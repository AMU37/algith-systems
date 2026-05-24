# core/models/company.py
from core import db
from datetime import datetime
import json

class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    commercial_reg = db.Column(db.String(50))
    activity = db.Column(db.String(100))
    business_type = db.Column(db.String(20), default='general')
    slogan = db.Column(db.String(200))
    primary_color = db.Column(db.String(7), default='#1a73e8')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # SaaS Fields
    subscription_status = db.Column(db.String(20), default='trial')
    subscription_end = db.Column(db.Date)
    is_blocked = db.Column(db.Boolean, default=False)
    plan_code = db.Column(db.String(50), default='trial')

    # Currency Settings
    currency = db.Column(db.String(10), default='YER')
    exchange_rate = db.Column(db.Float, default=1.0)
    currency_locked = db.Column(db.Boolean, default=False)

    # Relationships
    users = db.relationship('User', backref='company', lazy=True)
