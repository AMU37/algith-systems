# core/models/factory.py
from core import db
from datetime import datetime


class ProductionOrder(db.Model):
    __tablename__ = 'production_order'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class QualityCheck(db.Model):
    __tablename__ = 'quality_check'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    production_order_id = db.Column(db.Integer, db.ForeignKey('production_order.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    passed = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    production_order = db.relationship('ProductionOrder', backref='quality_checks')


class Machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    last_maintenance = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)