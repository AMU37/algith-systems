# core/models/subscription.py
from core import db
from datetime import datetime, date


class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    plan_code = db.Column(db.String(50), default='trial')
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date)
    monthly_price = db.Column(db.Float, default=0)
    max_users = db.Column(db.Integer, default=1)
    is_trial = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('Company', backref='subscriptions', lazy=True)


class Plan(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Float, default=0)
    yearly_price = db.Column(db.Float, default=0)
    max_users = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)


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

    company = db.relationship('Company', backref='payments', lazy=True)
    subscription = db.relationship('Subscription', backref='payments', lazy=True)