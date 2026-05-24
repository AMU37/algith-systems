# core/models/project.py
from core import db
from datetime import datetime


class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    contract_number = db.Column(db.String(50))
    contract_value = db.Column(db.Float, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='projects', lazy=True)


class Claim(db.Model):
    __tablename__ = 'claim'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    claim_number = db.Column(db.String(50))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    approved_amount = db.Column(db.Float, default=0)
    paid_amount = db.Column(db.Float, default=0)
    completion_percentage = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship('Project', backref='claims', lazy=True)


class MaterialPurchase(db.Model):
    __tablename__ = 'material_purchase'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    invoice_number = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supplier = db.relationship('Supplier', backref='material_purchases', lazy=True)
    project = db.relationship('Project', backref='material_purchases', lazy=True)


class MaterialItem(db.Model):
    __tablename__ = 'material_item'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('material_purchase.id'), nullable=False)
    material_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20))
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)