# core/models/restaurant.py
from core import db
from datetime import datetime


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0)
    cost = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TableOrder(db.Model):
    __tablename__ = 'table_order'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    table_number = db.Column(db.String(10))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('table_order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    item_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=1)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)