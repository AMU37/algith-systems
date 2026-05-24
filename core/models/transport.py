# core/models/transport.py
from core import db
from datetime import datetime


class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    capacity = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Trip(db.Model):
    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    from_location = db.Column(db.String(200))
    to_location = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    cost = db.Column(db.Float, default=0)
    revenue = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship('Vehicle', backref='trips')
    driver = db.relationship('Employee', foreign_keys=[driver_id])
    client = db.relationship('Client', backref='trips')


class FuelRecord(db.Model):
    __tablename__ = 'fuel_record'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Float)
    cost = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship('Vehicle', backref='fuel_records')


class VehicleMaintenance(db.Model):
    __tablename__ = 'vehicle_maintenance'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String(50))
    cost = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicle = db.relationship('Vehicle', backref='maintenance_records')