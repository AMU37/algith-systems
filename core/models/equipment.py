# core/models/equipment.py
from core import db
from datetime import datetime


class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EquipmentMaintenance(db.Model):
    __tablename__ = 'equipment_maintenance'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String(50))
    cost = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    equipment = db.relationship('Equipment', backref='maintenance_records')