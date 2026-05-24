# core/models/cleaning.py
from core import db
from datetime import datetime


class WorkSite(db.Model):
    __tablename__ = 'work_site'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    address = db.Column(db.String(200))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    worker_count = db.Column(db.Integer, default=0)
    work_hours = db.Column(db.String(50))
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref='work_sites')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])


class SupervisorReport(db.Model):
    __tablename__ = 'supervisor_report'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    report = db.Column(db.Text)
    issues = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    site = db.relationship('WorkSite', backref='reports')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])


class Visit(db.Model):
    __tablename__ = 'visit'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    visitor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    site = db.relationship('WorkSite', backref='visits')
    visitor = db.relationship('Employee', foreign_keys=[visitor_id])


class Complaint(db.Model):
    __tablename__ = 'complaint'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    resolution = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    client = db.relationship('Client', backref='complaints')
    site = db.relationship('WorkSite', backref='complaints')


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])
    site = db.relationship('WorkSite', backref='teams')


class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    team = db.relationship('Team', backref='members')
    employee = db.relationship('Employee')