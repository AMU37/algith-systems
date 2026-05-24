# core/models/school.py
from core import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    class_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    parent_name = db.Column(db.String(120))
    parent_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subject(db.Model):
    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.String(20), default='active')


class Exam(db.Model):
    __tablename__ = 'exam'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    score = db.Column(db.Float)
    max_score = db.Column(db.Float, default=100)
    date = db.Column(db.Date, default=datetime.utcnow)
    exam_type = db.Column(db.String(50))


class Fee(db.Model):
    __tablename__ = 'fee'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)