# core/models/accounting.py
from core import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    balance = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parent = db.relationship('Account', remote_side=[id], backref='children')


class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))
    entry_type = db.Column(db.String(50))
    reference = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class JournalLine(db.Model):
    __tablename__ = 'journal_line'

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('journal_entry.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.Column(db.String(100))
    description = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)

    entry = db.relationship('JournalEntry', backref='lines')
    account_ref = db.relationship('Account', backref='journal_lines')


class GLJournal(db.Model):
    __tablename__ = 'gl_journal'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))
    reference = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_debit = db.Column(db.Float, default=0)
    total_credit = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GLJournalLine(db.Model):
    __tablename__ = 'gl_journal_line'

    id = db.Column(db.Integer, primary_key=True)
    journal_id = db.Column(db.Integer, db.ForeignKey('gl_journal.id'), nullable=False)
    account_code = db.Column(db.String(20))
    account_name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)

    journal = db.relationship('GLJournal', backref='lines')


class Area(db.Model):
    __tablename__ = 'area'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)