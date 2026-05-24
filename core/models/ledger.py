# core/models/ledger.py
from core import db
from datetime import datetime


class LedgerEntry(db.Model):
    __tablename__ = 'ledger_entry'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    entry_date = db.Column(db.Date, default=datetime.utcnow)
    entry_number = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    reference_type = db.Column(db.String(50))
    reference_id = db.Column(db.Integer)
    total_debit = db.Column(db.Float, default=0)
    total_credit = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='posted')
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship('Company', backref='ledger_entries')
    lines = db.relationship('LedgerLine', backref='entry', lazy=True)


class LedgerLine(db.Model):
    __tablename__ = 'ledger_line'

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('ledger_entry.id'), nullable=False)
    account_code = db.Column(db.String(20))
    account_name = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)
    notes = db.Column(db.String(500))