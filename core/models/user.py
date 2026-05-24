# core/models/user.py
from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='user')
    permissions = db.Column(db.Text, default='{}')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('company_id', 'username', name='uq_company_username'),)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_permissions(self):
        return json.loads(self.permissions) if self.permissions else {}

    def has_permission(self, perm):
        if self.role == 'admin' or self.role == 'super_admin':
            return True
        return self.get_permissions().get(perm, False)
