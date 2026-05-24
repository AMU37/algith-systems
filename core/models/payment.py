# core/models/payment.py
from core import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))
    amount = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subscription = db.relationship('Subscription', backref='payments', lazy=True)
    company = db.relationship('Company', backref='payments', lazy=True)