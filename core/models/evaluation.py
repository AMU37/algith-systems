# core/models/evaluation.py
from core import db
from datetime import datetime

class Evaluation(db.Model):
    __tablename__ = 'evaluation'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    total_score = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EvaluationCriteria(db.Model):
    __tablename__ = 'evaluation_criteria'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    max_score = db.Column(db.Integer, default=5)
    weight = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    order_num = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EvaluationScore(db.Model):
    __tablename__ = 'evaluation_score'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('evaluation_criteria.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)