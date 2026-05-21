import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from functools import wraps
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'alghith-saas-2026-secret-key')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Database path - works on both local and PythonAnywhere
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'alghith.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = ''

BUSINESS_TYPES = {
    'service': {'name': 'شركة خدمات', 'icon': 'fa-briefcase', 'desc': 'شركة تقدم خدمات للشركات الأخرى'},
    'retail': {'name': 'متجر / بقالة / سوبر ماركت', 'icon': 'fa-store', 'desc': 'بيع وشراء المنتجات'},
    'trading': {'name': 'شركة تجارية', 'icon': 'fa-building', 'desc': 'استيراد وتصدير وتجارة عامة'},
    'contracting': {'name': 'شركة مقاولات', 'icon': 'fa-helmet-safety', 'desc': 'مقاولات وإنشاءات'},
    'restaurant': {'name': 'مطعم / كافتيريا', 'icon': 'fa-utensils', 'desc': 'خدمات طعام ومشروبات'},
    'general': {'name': 'أخرى', 'icon': 'fa-globe', 'desc': 'نشاط عام - جميع الوحدات متاحة'},
}

# ==================== MODELS ====================

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    commercial_reg = db.Column(db.String(50))
    activity = db.Column(db.String(100))
    business_type = db.Column(db.String(20), default='general')
    slogan = db.Column(db.String(200))
    primary_color = db.Column(db.String(7), default='#1a73e8')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # SaaS Fields
    subscription_status = db.Column(db.String(20), default='trial')
    subscription_end = db.Column(db.Date)
    is_blocked = db.Column(db.Boolean, default=False)
    plan_code = db.Column(db.String(50), default='trial')
    
    # Currency Settings
    currency = db.Column(db.String(10), default='YER')
    exchange_rate = db.Column(db.Float, default=1.0)
    currency_locked = db.Column(db.Boolean, default=False)
    
    users = db.relationship('User', backref='company', lazy=True)
    subscription = db.relationship('Subscription', backref='company', uselist=False, lazy=True)

class User(UserMixin, db.Model):
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
        if self.role == 'admin':
            return True
        return self.get_permissions().get(perm, False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(50))
    code = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    birth_place = db.Column(db.String(100))
    position = db.Column(db.String(100))
    join_date = db.Column(db.Date, default=datetime.utcnow)
    wage_type = db.Column(db.String(20), default='monthly')
    comprehensive_salary = db.Column(db.Float, default=0)
    basic_salary = db.Column(db.Float, default=0)
    daily_wage = db.Column(db.Float, default=0)
    area = db.Column(db.String(100), default='غير محدد')
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    deductions = db.relationship('Deduction', backref='employee', lazy=True)
    additions = db.relationship('Addition', backref='employee', lazy=True)
    evaluations = db.relationship('Evaluation', backref='employee', lazy=True)
    advances = db.relationship('Advance', backref='employee', lazy=True)
    salaries = db.relationship('Salary', backref='employee', lazy=True)

class Deduction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    reason = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    month = db.Column(db.String(7))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Addition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    reason = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    month = db.Column(db.String(7))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Advance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    amount = db.Column(db.Float, default=0)
    remaining = db.Column(db.Float, default=0)
    monthly_deduction = db.Column(db.Float, default=0)
    date = db.Column(db.Date, default=datetime.utcnow)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    total_score = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    scores = db.relationship('EvaluationScore', backref='evaluation', lazy=True)

class EvaluationCriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    max_score = db.Column(db.Integer, default=5)
    weight = db.Column(db.Float, default=1.0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    order = db.Column(db.Integer, default=0)

class EvaluationScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluation.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('evaluation_criteria.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    criteria = db.relationship('EvaluationCriteria', backref='scores')

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    month = db.Column(db.String(7), nullable=False)
    basic_salary = db.Column(db.Float, default=0)
    additions_total = db.Column(db.Float, default=0)
    deductions_total = db.Column(db.Float, default=0)
    advances_deduction = db.Column(db.Float, default=0)
    net_salary = db.Column(db.Float, default=0)
    is_paid = db.Column(db.Boolean, default=False)
    paid_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    balance = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contracts = db.relationship('Contract', backref='supplier', lazy=True)
    invoices = db.relationship('Invoice', backref='supplier', lazy=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    balance = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contracts = db.relationship('ClientContract', backref='client', lazy=True)
    invoices = db.relationship('SalesInvoice', backref='client', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    type = db.Column(db.String(20), default='product')
    unit = db.Column(db.String(20))
    purchase_price = db.Column(db.Float, default=0)
    sale_price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Float, default=0)
    min_quantity = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    invoice_number = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('PurchaseItem', backref='purchase', lazy=True)

class PurchaseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

class SalesInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    invoice_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('SalesInvoiceItem', backref='invoice', lazy=True)

class SalesInvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_invoice.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    invoice_number = db.Column(db.String(50))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    contract_number = db.Column(db.String(50))
    type = db.Column(db.String(20), default='monthly')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClientContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    contract_number = db.Column(db.String(50))
    type = db.Column(db.String(20), default='monthly')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))
    entry_type = db.Column(db.String(50))
    reference = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    lines = db.relationship('JournalLine', backref='entry', lazy=True)

class JournalLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('journal_entry.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.Column(db.String(100))
    description = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)

class GLJournal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))
    reference = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_debit = db.Column(db.Float, default=0)
    total_credit = db.Column(db.Float, default=0)
    company = db.relationship('Company', backref='gl_journals')
    lines = db.relationship('GLJournalLine', backref='journal', lazy=True)

class GLJournalLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journal_id = db.Column(db.Integer, db.ForeignKey('gl_journal.id'), nullable=False)
    account_code = db.Column(db.String(20))
    account_name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')

class Account(db.Model):
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
    children = db.relationship('Account', backref=db.backref('parent', remote_side=[id]), lazy=True)
    journal_lines = db.relationship('JournalLine', backref='account_ref', lazy=True)

    __table_args__ = (db.UniqueConstraint('company_id', 'code', name='uq_company_account'),)

# ==================== CONTRACTING MODELS ====================

class Project(db.Model):
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
    client = db.relationship('Client', backref='projects')
    claims = db.relationship('Claim', backref='project', lazy=True)

class Claim(db.Model):
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

class DailyAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='present')
    hours = db.Column(db.Float, default=0)
    daily_wage = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    employee = db.relationship('Employee', backref='attendances')
    project = db.relationship('Project', backref='attendances')

class DailyPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), default='cash')
    notes = db.Column(db.Text)
    employee = db.relationship('Employee', backref='daily_payments')
    project = db.relationship('Project', backref='daily_payments')

class MaterialPurchase(db.Model):
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
    supplier = db.relationship('Supplier', backref='material_purchases')
    project = db.relationship('Project', backref='material_purchases')
    items = db.relationship('MaterialItem', backref='purchase', lazy=True)

class MaterialItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('material_purchase.id'), nullable=False)
    material_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(20))
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

# ==================== RESTAURANT MODELS ====================

class MenuItem(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    table_number = db.Column(db.String(10))
    date = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('table_order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    item_name = db.Column(db.String(120))
    quantity = db.Column(db.Float, default=1)
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

# ==================== SERVICE MODELS ====================

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    contract_number = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    amount = db.Column(db.Float, default=0)
    terms = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client = db.relationship('Client', backref='service_contracts')

class ServiceOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    client = db.relationship('Client', backref='service_orders')
    service = db.relationship('Service', backref='orders')

# ==================== EQUIPMENT & TRANSPORT ====================

class Equipment(db.Model):
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

class EquipmentMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String(50))
    cost = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='completed')
    equipment = db.relationship('Equipment', backref='maintenance_records')

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    capacity = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)

class Trip(db.Model):
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
    vehicle = db.relationship('Vehicle', backref='trips')
    driver = db.relationship('Employee', foreign_keys=[driver_id])
    client = db.relationship('Client', backref='trips')

class FuelRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Float)
    cost = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    vehicle = db.relationship('Vehicle', backref='fuel_records')

class VehicleMaintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String(50))
    cost = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    vehicle = db.relationship('Vehicle', backref='maintenance_records')

# ==================== HOSPITAL ====================

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(120))
    blood_type = db.Column(db.String(5))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    license_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    time = db.Column(db.String(10))
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')

class LabTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    test_name = db.Column(db.String(120))
    date = db.Column(db.Date, default=datetime.utcnow)
    result = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    patient = db.relationship('Patient', backref='lab_tests')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Float, default=0)
    expiry_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')

# ==================== SCHOOL ====================

class Student(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.String(20), default='active')

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    score = db.Column(db.Float)
    max_score = db.Column(db.Float, default=100)
    date = db.Column(db.Date, default=datetime.utcnow)
    exam_type = db.Column(db.String(50))
    subject = db.relationship('Subject', backref='exams')
    student = db.relationship('Student', backref='exams')

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    amount = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    student = db.relationship('Student', backref='fees')

# ==================== FACTORY ====================

class ProductionOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)

class QualityCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    production_order_id = db.Column(db.Integer, db.ForeignKey('production_order.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    passed = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    last_maintenance = db.Column(db.Date)
    notes = db.Column(db.Text)

# ==================== CLEANING ====================

class WorkSite(db.Model):
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
    client = db.relationship('Client', backref='work_sites')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])

class SupervisorReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    report = db.Column(db.Text)
    issues = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted')
    site = db.relationship('WorkSite', backref='reports')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    visitor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)
    site = db.relationship('WorkSite', backref='visits')

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    resolution = db.Column(db.Text)
    client = db.relationship('Client', backref='complaints')
    site = db.relationship('WorkSite', backref='complaints')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('work_site.id'))
    status = db.Column(db.String(20), default='active')
    supervisor = db.relationship('Employee', foreign_keys=[supervisor_id])
    site = db.relationship('WorkSite', backref='teams')

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    team = db.relationship('Team', backref='members')
    employee = db.relationship('Employee')

# ==================== SAAS MODELS ====================

PLANS = {
    'trial': {'name': 'تجربة مجانية', 'price': 0, 'days': 14, 'max_users': 1, 'color': '#6c757d'},
    'basic': {'name': 'الباقة الأساسية', 'price': 3750, 'days': 30, 'max_users': 5, 'color': '#1a73e8'},
    'pro': {'name': 'الباقة الاحترافية', 'price': 8750, 'days': 30, 'max_users': 20, 'color': '#34a853'},
    'enterprise': {'name': 'المؤسسات', 'price': 24750, 'days': 30, 'max_users': 999, 'color': '#fbbc04'},
}

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    monthly_price = db.Column(db.Float, default=0)
    yearly_price = db.Column(db.Float, default=0)
    max_users = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    features = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    plan_code = db.Column(db.String(50), default='trial')
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    monthly_price = db.Column(db.Float, default=0)
    max_users = db.Column(db.Integer, default=1)
    is_trial = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))
    amount = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscription = db.relationship('Subscription', backref='payments', lazy=True)
    company = db.relationship('Company', backref='payments', lazy=True)

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    company = db.relationship('Company', backref='tickets', lazy=True)

# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_globals():
    try:
        if current_user.is_authenticated:
            try:
                company = current_user.company
            except Exception:
                company = None
            try:
                perms = current_user.get_permissions()
                modules = [p for p, v in perms.items() if v] if perms else []
            except Exception:
                modules = []
            bt = company.business_type if company else 'general'
            currency = company.currency if company else 'YER'
            exchange_rate = company.exchange_rate if company else 1.0
        else:
            company = None
            modules = []
            bt = 'general'
            currency = 'YER'
            exchange_rate = 1.0
    except Exception:
        company = None
        modules = []
        bt = 'general'
        currency = 'YER'
        exchange_rate = 1.0
    return {'now': date.today().isoformat(), 'company': company, 'modules': modules, 'business_type': bt, 'currency': currency, 'exchange_rate': exchange_rate}

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ==================== HELPERS ====================

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('غير مصرح لك بالوصول', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission):
                flash('غير مصرح لك بالوصول', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator

def cid():
    return current_user.company_id

def get_account(company_id, account_type):
    acc = Account.query.filter_by(company_id=company_id, type=account_type).first()
    if not acc:
        defaults = {
            'cash': {'code': '101', 'name': 'الصندوق'},
            'bank': {'code': '102', 'name': 'البنك'},
            'receivables': {'code': '110', 'name': 'ذمم العملاء'},
            'payables': {'code': '210', 'name': 'ذمم الموردين'},
            'employee_advances': {'code': '115', 'name': 'سلف الموظفين'},
            'expenses': {'code': '501', 'name': 'المصروفات'},
            'salary_expenses': {'code': '510', 'name': 'مصروفات الرواتب'},
            'revenue': {'code': '401', 'name': 'الإيرادات'},
            'purchases': {'code': '502', 'name': 'المشتريات'},
        }
        d = defaults.get(account_type, {'code': '000', 'name': account_type})
        acc = Account(company_id=company_id, code=d['code'], name=d['name'], type=account_type)
        db.session.add(acc)
        db.session.flush()
    return acc

def add_journal_entry(description, amount, entry_type, account_type=None, ref_account_type=None):
    entry = JournalEntry(company_id=cid(), date=date.today(), description=description, entry_type=entry_type, created_by=current_user.id)
    db.session.add(entry)
    db.session.flush()
    
    if entry_type in ['purchase', 'supplier_invoice', 'advance']:
        debit_acc = get_account(cid(), 'purchases' if entry_type == 'purchase' else 'employee_advances')
        credit_acc = get_account(cid(), 'cash')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
        if ref_account_type:
            ref_acc = get_account(cid(), ref_account_type)
            ref_acc.balance += amount
    elif entry_type in ['sale', 'sale_payment']:
        debit_acc = get_account(cid(), 'cash')
        credit_acc = get_account(cid(), 'revenue')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
    elif entry_type == 'salary':
        debit_acc = get_account(cid(), 'salary_expenses')
        credit_acc = get_account(cid(), 'cash')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
    elif entry_type == 'employee':
        debit_acc = get_account(cid(), 'expenses')
        credit_acc = get_account(cid(), 'cash')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
    elif entry_type == 'deduction':
        debit_acc = get_account(cid(), 'cash')
        credit_acc = get_account(cid(), 'salary_expenses')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
    elif entry_type == 'addition':
        debit_acc = get_account(cid(), 'salary_expenses')
        credit_acc = get_account(cid(), 'cash')
        db.session.add(JournalLine(entry_id=entry.id, account_id=debit_acc.id, account=debit_acc.name, description=description, debit=amount, credit=0))
        db.session.add(JournalLine(entry_id=entry.id, account_id=credit_acc.id, account=credit_acc.name, description=description, debit=0, credit=amount))
    
    db.session.flush()
    return entry

# ==================== AUTH ====================

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    try:
        if current_user.is_authenticated:
            if current_user.role == 'super_admin':
                return redirect(url_for('super_admin_dashboard'))
            return redirect(url_for('dashboard'))
    except Exception:
        pass
    if request.method == 'POST':
        try:
            company_name = request.form.get('company_name', '').strip()
            admin_username = request.form.get('admin_username', '').strip()
            admin_password = request.form.get('admin_password', '').strip()
            if not company_name:
                flash('اسم الشركة مطلوب', 'error')
                return redirect(url_for('setup'))
            if not admin_username:
                flash('اسم المستخدم مطلوب', 'error')
                return redirect(url_for('setup'))
            if not admin_password:
                flash('كلمة المرور مطلوبة', 'error')
                return redirect(url_for('setup'))
            code = request.form.get('company_code', '').strip()
            if not code:
                code = f"C{Company.query.count() + 1:04d}"
            if Company.query.filter_by(code=code).first():
                flash('رمز الشركة مستخدم بالفعل', 'error')
                return redirect(url_for('setup'))
            company = Company(
                name=company_name, code=code, phone=request.form.get('phone', ''),
                email=request.form.get('email', ''), address=request.form.get('address', ''),
                tax_number=request.form.get('tax_number', ''), commercial_reg=request.form.get('commercial_reg', ''),
                activity=request.form.get('activity', ''), slogan=request.form.get('slogan', ''),
                business_type=request.form.get('business_type', 'general'),
                primary_color=request.form.get('primary_color', '#1a73e8')
            )
            db.session.add(company); db.session.flush()
            admin = User(
                company_id=company.id, username=admin_username, full_name='مدير النظام',
                role='admin', is_active=True,
                permissions=json.dumps({p: True for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin','projects','claims','attendance','daily_payments','materials','menu','orders','services','service_contracts','service_orders','equipment','fuel','patients','doctors','appointments','lab','medicines','students','subjects','exams','fees','vehicles','trips','production_orders','quality','machines','work_sites','teams','visits','supervisor_reports','complaints']})
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            
            plan_code = request.form.get('plan_code', 'trial')
            plan_info = PLANS.get(plan_code, PLANS['trial'])
            sub = Subscription(
                company_id=company.id, plan_code=plan_code, status='active',
                start_date=date.today(), end_date=date.today() + timedelta(days=plan_info.get('days', 14)),
                monthly_price=plan_info['price'], max_users=plan_info['max_users'], is_trial=(plan_code == 'trial')
            )
            db.session.add(sub)
            company.subscription_status = 'trial' if plan_code == 'trial' else 'active'
            company.subscription_end = sub.end_date
            company.plan_code = plan_code
            
            # Create default accounts for the company
            default_accounts = [
                ('1001', 'الصندوق الرئيسي', 'cash', 0),
                ('1002', 'البنك', 'bank', 0),
                ('1101', 'الذمم المدينة', 'receivables', 0),
                ('2001', 'الذمم الدائنة', 'payables', 0),
                ('3001', 'رأس المال', 'equity', 0),
                ('4001', 'إيرادات المبيعات', 'revenue', 0),
                ('5001', 'تكلفة المبيعات', 'expense', 0),
                ('5002', 'المصروفات التشغيلية', 'expense', 0),
            ]
            for code, name, acc_type, balance in default_accounts:
                acc = Account(company_id=company.id, code=code, name=name, type=acc_type, balance=balance, status='active')
                db.session.add(acc)
            
            db.session.commit()
            login_user(admin)
            flash('تم إنشاء حسابك وتسجيل الدخول بنجاح!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطأ: {str(e)}', 'error')
            return redirect(url_for('setup'))
    return render_template('setup.html', business_types=BUSINESS_TYPES, plans=PLANS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.is_authenticated:
            if current_user.role == 'super_admin':
                return redirect(url_for('super_admin_dashboard'))
            return redirect(url_for('dashboard'))
    except Exception:
        pass
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_active:
            if user.role == 'super_admin':
                login_user(user)
                return redirect(url_for('super_admin_dashboard'))
            try:
                if user.company.is_active:
                    login_user(user)
                    return redirect(url_for('dashboard'))
            except Exception:
                flash('حسابك غير مرتبط بشركة صالحة', 'error')
                return redirect(url_for('login'))
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.before_request
def check_subscription():
    if not current_user.is_authenticated:
        return None
    if current_user.role == 'super_admin':
        return None
    try:
        company = current_user.company
        if not company:
            return None
        if company.is_blocked:
            if request.endpoint not in ['subscription_expired', 'static', 'logout']:
                return redirect(url_for('subscription_expired'))
        if company.subscription_end and date.today() > company.subscription_end:
            company.is_blocked = True
            company.subscription_status = 'expired'
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
            if request.endpoint not in ['subscription_expired', 'static', 'logout']:
                return redirect(url_for('subscription_expired'))
    except Exception:
        db.session.rollback()
    return None

# ==================== DASHBOARD ====================

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'super_admin':
        return redirect(url_for('super_admin_dashboard'))
    try:
        c = cid()
    except Exception:
        flash('خطأ في تحميل بيانات الشركة', 'error')
        return redirect(url_for('logout'))
    bt = current_user.company.business_type if current_user.company else 'general'
    employees_count = Employee.query.filter_by(company_id=c, status='active').count()
    suppliers_count = Supplier.query.filter_by(company_id=c, status='active').count()
    clients_count = Client.query.filter_by(company_id=c, status='active').count()
    products_count = Product.query.filter_by(company_id=c, status='active').count()
    today = date.today().strftime('%Y-%m')
    month_salaries = Salary.query.filter_by(company_id=c, month=today).all()
    total_salaries = sum(s.net_salary for s in month_salaries)
    total_purchases = db.session.query(db.func.sum(Purchase.total)).filter_by(company_id=c).scalar() or 0
    total_sales = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=c).scalar() or 0
    recent_sales = SalesInvoice.query.filter_by(company_id=c).order_by(SalesInvoice.date.desc()).limit(10).all()
    recent_purchases = Purchase.query.filter_by(company_id=c).order_by(Purchase.date.desc()).limit(10).all()
    kwargs = {
        'employees_count': employees_count, 'suppliers_count': suppliers_count,
        'clients_count': clients_count, 'products_count': products_count,
        'total_salaries': total_salaries, 'total_purchases': total_purchases,
        'total_sales': total_sales, 'recent_sales': recent_sales,
        'recent_purchases': recent_purchases, 'business_type': bt
    }
    if bt == 'contracting':
        kwargs['projects_count'] = Project.query.filter_by(company_id=c, status='active').count()
        kwargs['pending_claims'] = Claim.query.filter_by(company_id=c, status='pending').count()
        kwargs['total_claims'] = db.session.query(db.func.sum(Claim.amount)).filter_by(company_id=c).scalar() or 0
        kwargs['total_paid_claims'] = db.session.query(db.func.sum(Claim.paid_amount)).filter_by(company_id=c).scalar() or 0
        kwargs['today_attendance'] = DailyAttendance.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['recent_claims'] = Claim.query.filter_by(company_id=c).order_by(Claim.date.desc()).limit(5).all()
        kwargs['recent_projects'] = Project.query.filter_by(company_id=c).order_by(Project.created_at.desc()).limit(5).all()
    elif bt == 'restaurant':
        kwargs['menu_count'] = MenuItem.query.filter_by(company_id=c, status='active').count()
        kwargs['today_orders'] = TableOrder.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['today_revenue'] = db.session.query(db.func.sum(TableOrder.total)).filter_by(company_id=c, date=date.today()).scalar() or 0
        kwargs['pending_orders'] = TableOrder.query.filter_by(company_id=c, status='pending').count()
        kwargs['recent_orders'] = TableOrder.query.filter_by(company_id=c).order_by(TableOrder.date.desc()).limit(10).all()
    elif bt == 'hospital':
        kwargs['patients_count'] = Patient.query.filter_by(company_id=c).count()
        kwargs['doctors_count'] = Doctor.query.filter_by(company_id=c, status='active').count()
        kwargs['today_appointments'] = Appointment.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['pending_appointments'] = Appointment.query.filter_by(company_id=c, status='scheduled').count()
        kwargs['recent_appointments'] = Appointment.query.filter_by(company_id=c).order_by(Appointment.date.desc()).limit(10).all()
    elif bt == 'school':
        kwargs['students_count'] = Student.query.filter_by(company_id=c, status='active').count()
        kwargs['subjects_count'] = Subject.query.filter_by(company_id=c, status='active').count()
        kwargs['total_fees'] = db.session.query(db.func.sum(Fee.amount)).filter_by(company_id=c).scalar() or 0
        kwargs['pending_fees'] = Fee.query.filter_by(company_id=c, status='pending').count()
        kwargs['recent_exams'] = Exam.query.filter_by(company_id=c).order_by(Exam.date.desc()).limit(10).all()
    elif bt == 'transport':
        kwargs['vehicles_count'] = Vehicle.query.filter_by(company_id=c, status='active').count()
        kwargs['today_trips'] = Trip.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['total_revenue'] = db.session.query(db.func.sum(Trip.revenue)).filter_by(company_id=c).scalar() or 0
        kwargs['pending_trips'] = Trip.query.filter_by(company_id=c, status='pending').count()
        kwargs['recent_trips'] = Trip.query.filter_by(company_id=c).order_by(Trip.date.desc()).limit(10).all()
    elif bt == 'factory':
        kwargs['production_orders'] = ProductionOrder.query.filter_by(company_id=c).count()
        kwargs['machines_count'] = Machine.query.filter_by(company_id=c, status='active').count()
        kwargs['quality_checks'] = QualityCheck.query.filter_by(company_id=c).count()
        kwargs['recent_orders'] = ProductionOrder.query.filter_by(company_id=c).order_by(ProductionOrder.start_date.desc()).limit(10).all()
    elif bt == 'retail':
        kwargs['products_count'] = Product.query.filter_by(company_id=c, status='active').count()
        kwargs['today_sales'] = SalesInvoice.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['today_revenue'] = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=c, date=date.today()).scalar() or 0
        kwargs['low_stock'] = Product.query.filter(Product.company_id == c, Product.quantity <= Product.min_quantity).count()
        kwargs['recent_sales'] = SalesInvoice.query.filter_by(company_id=c).order_by(SalesInvoice.date.desc()).limit(10).all()
    elif bt == 'cleaning':
        kwargs['clients_count'] = Client.query.filter_by(company_id=c, status='active').count()
        kwargs['teams_count'] = Team.query.filter_by(company_id=c, status='active').count()
        kwargs['active_contracts'] = ClientContract.query.filter_by(company_id=c, status='active').count()
        kwargs['today_visits'] = Visit.query.filter_by(company_id=c, date=date.today()).count()
        kwargs['recent_visits'] = Visit.query.filter_by(company_id=c).order_by(Visit.date.desc()).limit(10).all()
    elif bt == 'trading':
        kwargs['suppliers_count'] = suppliers_count
        kwargs['clients_count'] = clients_count
        kwargs['total_purchases'] = total_purchases
        kwargs['total_sales'] = total_sales
        kwargs['recent_sales'] = SalesInvoice.query.filter_by(company_id=c).order_by(SalesInvoice.date.desc()).limit(10).all()
        kwargs['recent_purchases'] = Purchase.query.filter_by(company_id=c).order_by(Purchase.date.desc()).limit(10).all()
    elif bt == 'service':
        kwargs['services_count'] = Service.query.filter_by(company_id=c, status='active').count()
        kwargs['active_contracts'] = ServiceContract.query.filter_by(company_id=c, status='active').count()
        kwargs['pending_orders'] = ServiceOrder.query.filter_by(company_id=c, status='pending').count()
        kwargs['total_revenue'] = db.session.query(db.func.sum(ServiceOrder.amount)).filter_by(company_id=c).scalar() or 0
        kwargs['recent_orders'] = ServiceOrder.query.filter_by(company_id=c).order_by(ServiceOrder.date.desc()).limit(10).all()
    return render_template('dashboard.html', **kwargs)

# ==================== EMPLOYEES ====================

@app.route('/employees')
@login_required
@permission_required('employees')
def employees():
    emps = Employee.query.filter_by(company_id=cid()).all()
    areas = Area.query.filter_by(company_id=cid(), status='active').all()
    return render_template('employees.html', employees=emps, areas=areas)

@app.route('/employee/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_employee():
    wage_type = request.form.get('wage_type', 'monthly')
    daily_wage = float(request.form.get('daily_wage') or 0)
    comprehensive_salary = float(request.form.get('comprehensive_salary') or 0)
    basic_salary = float(request.form.get('basic_salary') or 0)
    if wage_type == 'daily' and daily_wage > 0:
        comprehensive_salary = daily_wage * 30
        basic_salary = daily_wage * 26
    emp = Employee(company_id=cid(), name=request.form.get('name'), card_number=request.form.get('card_number'),
        code=request.form.get('code'), birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None,
        birth_place=request.form.get('birth_place'), position=request.form.get('position'),
        join_date=datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date() if request.form.get('join_date') else date.today(),
        wage_type=wage_type, comprehensive_salary=comprehensive_salary, basic_salary=basic_salary, daily_wage=daily_wage,
        area=request.form.get('area'), notes=request.form.get('notes'))
    db.session.add(emp); db.session.flush()
    if request.form.get('create_user') == 'on':
        un = request.form.get('user_username') or emp.code or f"emp_{emp.id}"
        up = request.form.get('user_password') or '123456'
        if not User.query.filter_by(company_id=cid(), username=un).first():
            u = User(company_id=cid(), username=un, full_name=emp.name, role='user',
                    permissions=json.dumps({p: False for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin','projects','claims','attendance','daily_payments','materials','menu','orders','services','service_contracts','service_orders']}))
            u.set_password(up); db.session.add(u)
    db.session.commit()
    flash('تم إضافة الموظف بنجاح', 'success')
    return redirect(url_for('employees'))

@app.route('/employee/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('employees')
def edit_employee(id):
    emp = db.session.get(Employee, id)
    if not emp or emp.company_id != cid(): return redirect(url_for('employees'))
    emp.name = request.form.get('name'); emp.card_number = request.form.get('card_number')
    emp.code = request.form.get('code')
    emp.birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None
    emp.birth_place = request.form.get('birth_place'); emp.position = request.form.get('position')
    emp.join_date = datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date() if request.form.get('join_date') else emp.join_date
    emp.wage_type = request.form.get('wage_type', 'monthly')
    emp.daily_wage = float(request.form.get('daily_wage') or 0)
    emp.comprehensive_salary = float(request.form.get('comprehensive_salary') or 0)
    emp.basic_salary = float(request.form.get('basic_salary') or 0)
    if emp.wage_type == 'daily' and emp.daily_wage > 0:
        emp.comprehensive_salary = emp.daily_wage * 30
        emp.basic_salary = emp.daily_wage * 26
    emp.area = request.form.get('area'); emp.status = request.form.get('status', 'active')
    emp.notes = request.form.get('notes'); db.session.commit()
    flash('تم تعديل بيانات الموظف بنجاح', 'success')
    return redirect(url_for('employees'))

@app.route('/employee/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('employees')
def delete_employee(id):
    emp = db.session.get(Employee, id)
    if emp and emp.company_id == cid(): emp.status = 'deleted'; db.session.commit()
    flash('تم حذف الموظف', 'success')
    return redirect(url_for('employees'))

# ==================== DEDUCTIONS & ADDITIONS ====================

@app.route('/deductions')
@login_required
@permission_required('employees')
def deductions():
    d = Deduction.query.filter_by(company_id=cid()).order_by(Deduction.date.desc()).all()
    e = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('deductions.html', deductions=d, employees=e)

@app.route('/deduction/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_deduction():
    ded = Deduction(company_id=cid(), employee_id=int(request.form.get('employee_id')), type=request.form.get('type'),
        amount=float(request.form.get('amount') or 0), reason=request.form.get('reason'),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        month=request.form.get('month', date.today().strftime('%Y-%m')), created_by=current_user.id)
    db.session.add(ded); add_journal_entry(f'خصم {ded.type}', ded.amount, 'deduction')
    db.session.commit()
    flash('تم إضافة الخصم بنجاح', 'success')
    return redirect(url_for('deductions'))

@app.route('/additions')
@login_required
@permission_required('employees')
def additions():
    a = Addition.query.filter_by(company_id=cid()).order_by(Addition.date.desc()).all()
    e = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('additions.html', additions=a, employees=e)

@app.route('/addition/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_addition():
    add = Addition(company_id=cid(), employee_id=int(request.form.get('employee_id')), type=request.form.get('type'),
        amount=float(request.form.get('amount') or 0), reason=request.form.get('reason'),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        month=request.form.get('month', date.today().strftime('%Y-%m')), created_by=current_user.id)
    db.session.add(add); add_journal_entry(f'إضافة {add.type}', add.amount, 'addition')
    db.session.commit()
    flash('تم إضافة الإضافة بنجاح', 'success')
    return redirect(url_for('additions'))

@app.route('/advances')
@login_required
@permission_required('employees')
def advances():
    a = Advance.query.filter_by(company_id=cid()).order_by(Advance.date.desc()).all()
    e = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('advances.html', advances=a, employees=e)

@app.route('/advance/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_advance():
    amount = float(request.form.get('amount') or 0)
    adv = Advance(company_id=cid(), employee_id=int(request.form.get('employee_id')), amount=amount, remaining=amount,
        monthly_deduction=float(request.form.get('monthly_deduction') or 0),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        notes=request.form.get('notes'))
    db.session.add(adv); add_journal_entry('سلفة موظف', amount, 'advance')
    db.session.commit()
    flash('تم إضافة السلفة بنجاح', 'success')
    return redirect(url_for('advances'))

# ==================== SALARIES ====================

@app.route('/salaries')
@login_required
@permission_required('salaries')
def salaries():
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    emps = Employee.query.filter_by(company_id=cid(), status='active').all()
    salary_data = []
    for emp in emps:
        salary = Salary.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).first()
        if salary:
            salary_data.append({'employee': emp, 'salary': salary})
        else:
            d = Deduction.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).all()
            a = Addition.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).all()
            adv = Advance.query.filter_by(company_id=cid(), employee_id=emp.id, status='active').all()
            td = sum(x.amount for x in d); ta = sum(x.amount for x in a); ad = sum(x.monthly_deduction for x in adv)
            base = emp.comprehensive_salary if emp.wage_type == 'monthly' else (emp.daily_wage * 30)
            salary_data.append({'employee': emp, 'salary': None, 'total_deductions': td, 'total_additions': ta, 'advances_deduction': ad, 'net': base + ta - td - ad})
    return render_template('salaries.html', salary_data=salary_data, month=month)

@app.route('/salary/generate/<month>', methods=['POST'])
@login_required
@permission_required('salaries')
def generate_salaries(month):
    emps = Employee.query.filter_by(company_id=cid(), status='active').all()
    for emp in emps:
        if Salary.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).first(): continue
        d = Deduction.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).all()
        a = Addition.query.filter_by(company_id=cid(), employee_id=emp.id, month=month).all()
        adv = Advance.query.filter_by(company_id=cid(), employee_id=emp.id, status='active').all()
        td = sum(x.amount for x in d); ta = sum(x.amount for x in a); ad = sum(x.monthly_deduction for x in adv)
        base = emp.comprehensive_salary if emp.wage_type == 'monthly' else (emp.daily_wage * 30)
        net = base + ta - td - ad
        salary = Salary(company_id=cid(), employee_id=emp.id, month=month, basic_salary=emp.basic_salary,
            additions_total=ta, deductions_total=td, advances_deduction=ad, net_salary=net)
        db.session.add(salary)
        for av in adv:
            if av.remaining > 0: av.remaining -= min(av.monthly_deduction, av.remaining)
    db.session.commit()
    flash('تم إنشاء الرواتب بنجاح', 'success')
    return redirect(url_for('salaries', month=month))

@app.route('/salary/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('salaries')
def pay_salary(id):
    salary = db.session.get(Salary, id)
    if salary and salary.company_id == cid():
        salary.is_paid = True; salary.paid_date = date.today()
        add_journal_entry(f'صرف راتب - {salary.employee.name} - {salary.month}', salary.net_salary, 'salary')
        cash_acc = get_account(cid(), 'cash')
        cash_acc.balance -= salary.net_salary
        db.session.commit()
        flash('تم صرف الراتب بنجاح', 'success')
    return redirect(url_for('salaries'))

# ==================== EVALUATIONS ====================

@app.route('/evaluation-criteria')
@login_required
@permission_required('employees')
def evaluation_criteria():
    c = EvaluationCriteria.query.filter_by(company_id=cid()).order_by(EvaluationCriteria.order).all()
    return render_template('evaluation_criteria.html', criteria=c)

@app.route('/evaluation-criteria/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_evaluation_criteria():
    ec = EvaluationCriteria(company_id=cid(), name=request.form.get('name'), max_score=int(request.form.get('max_score') or 5),
        weight=float(request.form.get('weight') or 1.0), description=request.form.get('description'), order=int(request.form.get('order') or 0))
    db.session.add(ec); db.session.commit()
    flash('تم إضافة معيار التقييم بنجاح', 'success')
    return redirect(url_for('evaluation_criteria'))

@app.route('/evaluation-criteria/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('employees')
def edit_evaluation_criteria(id):
    ec = db.session.get(EvaluationCriteria, id)
    if ec and ec.company_id == cid():
        ec.name = request.form.get('name'); ec.max_score = int(request.form.get('max_score') or 5)
        ec.weight = float(request.form.get('weight') or 1.0); ec.description = request.form.get('description')
        ec.order = int(request.form.get('order') or 0); ec.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل معيار التقييم بنجاح', 'success')
    return redirect(url_for('evaluation_criteria'))

@app.route('/evaluation-criteria/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('employees')
def delete_evaluation_criteria(id):
    ec = db.session.get(EvaluationCriteria, id)
    if ec and ec.company_id == cid(): db.session.delete(ec); db.session.commit()
    flash('تم حذف معيار التقييم', 'success')
    return redirect(url_for('evaluation_criteria'))

@app.route('/evaluations')
@login_required
@permission_required('employees')
def evaluations():
    today = request.args.get('date', date.today().isoformat())
    ev = Evaluation.query.filter_by(company_id=cid(), date=today).all()
    emps = Employee.query.filter_by(company_id=cid(), status='active').all()
    crit = EvaluationCriteria.query.filter_by(company_id=cid(), status='active').order_by(EvaluationCriteria.order).all()
    return render_template('evaluations.html', evaluations=ev, employees=emps, today=today, criteria=crit)

@app.route('/evaluation/add', methods=['POST'])
@login_required
@permission_required('employees')
def add_evaluation():
    ev = Evaluation(company_id=cid(), employee_id=int(request.form.get('employee_id')),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(), total_score=0,
        notes=request.form.get('notes'), evaluator_id=current_user.id)
    db.session.add(ev); db.session.flush()
    crit = EvaluationCriteria.query.filter_by(company_id=cid(), status='active').all()
    total = 0
    for c in crit:
        sv = float(request.form.get(f'score_{c.id}') or 0); total += sv
        es = EvaluationScore(evaluation_id=ev.id, criteria_id=c.id, score=sv, notes=request.form.get(f'score_notes_{c.id}', ''))
        db.session.add(es)
    ev.total_score = total; db.session.commit()
    flash('تم إضافة التقييم بنجاح', 'success')
    return redirect(url_for('evaluations'))

# ==================== AREAS ====================

@app.route('/areas')
@login_required
@permission_required('areas')
def areas():
    a = Area.query.filter_by(company_id=cid()).all()
    return render_template('areas.html', areas=a)

@app.route('/area/add', methods=['POST'])
@login_required
@permission_required('areas')
def add_area():
    area = Area(company_id=cid(), name=request.form.get('name'), description=request.form.get('description'))
    db.session.add(area); db.session.commit()
    flash('تم إضافة المنطقة بنجاح', 'success')
    return redirect(url_for('areas'))

@app.route('/area/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('areas')
def edit_area(id):
    area = db.session.get(Area, id)
    if area and area.company_id == cid():
        area.name = request.form.get('name'); area.description = request.form.get('description')
        area.status = request.form.get('status', 'active'); db.session.commit()
        flash('تم تعديل المنطقة بنجاح', 'success')
    return redirect(url_for('areas'))

@app.route('/area/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('areas')
def delete_area(id):
    area = db.session.get(Area, id)
    if area and area.company_id == cid(): db.session.delete(area); db.session.commit()
    flash('تم حذف المنطقة', 'success')
    return redirect(url_for('areas'))

# ==================== SUPPLIERS ====================

@app.route('/suppliers')
@login_required
@permission_required('suppliers')
def suppliers():
    s = Supplier.query.filter_by(company_id=cid()).all()
    return render_template('suppliers.html', suppliers=s)

@app.route('/supplier/add', methods=['POST'])
@login_required
@permission_required('suppliers')
def add_supplier():
    s = Supplier(company_id=cid(), name=request.form.get('name'), company_name=request.form.get('company'),
        phone=request.form.get('phone'), email=request.form.get('email'), address=request.form.get('address'),
        tax_number=request.form.get('tax_number'), notes=request.form.get('notes'))
    db.session.add(s); db.session.commit()
    flash('تم إضافة المورد بنجاح', 'success')
    return redirect(url_for('suppliers'))

@app.route('/supplier/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('suppliers')
def edit_supplier(id):
    s = db.session.get(Supplier, id)
    if s and s.company_id == cid():
        s.name = request.form.get('name'); s.company_name = request.form.get('company')
        s.phone = request.form.get('phone'); s.email = request.form.get('email')
        s.address = request.form.get('address'); s.tax_number = request.form.get('tax_number')
        s.balance = float(request.form.get('balance') or 0); s.status = request.form.get('status', 'active')
        s.notes = request.form.get('notes'); db.session.commit()
        flash('تم تعديل المورد بنجاح', 'success')
    return redirect(url_for('suppliers'))

@app.route('/supplier/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('suppliers')
def delete_supplier(id):
    s = db.session.get(Supplier, id)
    if s and s.company_id == cid(): s.status = 'deleted'; db.session.commit()
    flash('تم حذف المورد', 'success')
    return redirect(url_for('suppliers'))

@app.route('/supplier-contracts')
@login_required
@permission_required('suppliers')
def supplier_contracts():
    c = Contract.query.filter_by(company_id=cid()).order_by(Contract.created_at.desc()).all()
    s = Supplier.query.filter_by(company_id=cid(), status='active').all()
    return render_template('supplier_contracts.html', contracts=c, suppliers=s)

@app.route('/supplier-contract/add', methods=['POST'])
@login_required
@permission_required('suppliers')
def add_supplier_contract():
    c = Contract(company_id=cid(), supplier_id=int(request.form.get('supplier_id')),
        contract_number=request.form.get('contract_number'), type=request.form.get('type'),
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else date.today(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        amount=float(request.form.get('amount') or 0), terms=request.form.get('terms'))
    db.session.add(c); db.session.commit()
    flash('تم إضافة العقد بنجاح', 'success')
    return redirect(url_for('supplier_contracts'))

@app.route('/supplier-contract/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('suppliers')
def delete_supplier_contract(id):
    c = db.session.get(Contract, id)
    if c and c.company_id == cid(): db.session.delete(c); db.session.commit()
    flash('تم حذف العقد', 'success')
    return redirect(url_for('supplier_contracts'))

@app.route('/supplier-invoices')
@login_required
@permission_required('suppliers')
def supplier_invoices():
    i = Invoice.query.filter_by(company_id=cid()).order_by(Invoice.date.desc()).all()
    s = Supplier.query.filter_by(company_id=cid(), status='active').all()
    return render_template('supplier_invoices.html', invoices=i, suppliers=s)

@app.route('/supplier-invoice/add', methods=['POST'])
@login_required
@permission_required('suppliers')
def add_supplier_invoice():
    inv = Invoice(company_id=cid(), supplier_id=int(request.form.get('supplier_id')), invoice_number=request.form.get('invoice_number'),
        amount=float(request.form.get('amount') or 0), paid=float(request.form.get('paid') or 0),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        notes=request.form.get('notes'), created_by=current_user.id)
    inv.status = 'paid' if inv.paid >= inv.amount else 'pending'
    db.session.add(inv)
    supplier = db.session.get(Supplier, inv.supplier_id)
    if supplier: supplier.balance += inv.amount - inv.paid
    add_journal_entry(f'فاتورة مورد', inv.amount, 'supplier_invoice')
    db.session.commit()
    flash('تم إضافة الفاتورة بنجاح', 'success')
    return redirect(url_for('supplier_invoices'))

@app.route('/supplier-invoice/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('suppliers')
def delete_supplier_invoice(id):
    inv = db.session.get(Invoice, id)
    if inv and inv.company_id == cid():
        supplier = db.session.get(Supplier, inv.supplier_id)
        if supplier: supplier.balance -= (inv.amount - inv.paid)
        db.session.delete(inv); db.session.commit()
        flash('تم حذف الفاتورة', 'success')
    return redirect(url_for('supplier_invoices'))

# ==================== CLIENTS ====================

@app.route('/clients')
@login_required
@permission_required('clients')
def clients():
    c = Client.query.filter_by(company_id=cid()).all()
    return render_template('clients.html', clients=c)

@app.route('/client/add', methods=['POST'])
@login_required
@permission_required('clients')
def add_client():
    c = Client(company_id=cid(), name=request.form.get('name'), company_name=request.form.get('company'),
        phone=request.form.get('phone'), email=request.form.get('email'), address=request.form.get('address'),
        tax_number=request.form.get('tax_number'), notes=request.form.get('notes'))
    db.session.add(c); db.session.commit()
    flash('تم إضافة العميل بنجاح', 'success')
    return redirect(url_for('clients'))

@app.route('/client/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('clients')
def edit_client(id):
    c = db.session.get(Client, id)
    if c and c.company_id == cid():
        c.name = request.form.get('name'); c.company_name = request.form.get('company')
        c.phone = request.form.get('phone'); c.email = request.form.get('email')
        c.address = request.form.get('address'); c.tax_number = request.form.get('tax_number')
        c.balance = float(request.form.get('balance') or 0); c.status = request.form.get('status', 'active')
        c.notes = request.form.get('notes'); db.session.commit()
        flash('تم تعديل العميل بنجاح', 'success')
    return redirect(url_for('clients'))

@app.route('/client/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('clients')
def delete_client(id):
    c = db.session.get(Client, id)
    if c and c.company_id == cid(): c.status = 'deleted'; db.session.commit()
    flash('تم حذف العميل', 'success')
    return redirect(url_for('clients'))

@app.route('/client-contracts')
@login_required
@permission_required('clients')
def client_contracts():
    c = ClientContract.query.filter_by(company_id=cid()).order_by(ClientContract.created_at.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    return render_template('client_contracts.html', contracts=c, clients=cl)

@app.route('/client-contract/add', methods=['POST'])
@login_required
@permission_required('clients')
def add_client_contract():
    c = ClientContract(company_id=cid(), client_id=int(request.form.get('client_id')),
        contract_number=request.form.get('contract_number'), type=request.form.get('type'),
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else date.today(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        amount=float(request.form.get('amount') or 0), terms=request.form.get('terms'))
    db.session.add(c); db.session.commit()
    flash('تم إضافة العقد بنجاح', 'success')
    return redirect(url_for('client_contracts'))

@app.route('/client-contract/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('clients')
def delete_client_contract(id):
    c = db.session.get(ClientContract, id)
    if c and c.company_id == cid(): db.session.delete(c); db.session.commit()
    flash('تم حذف العقد', 'success')
    return redirect(url_for('client_contracts'))

# ==================== PRODUCTS ====================

@app.route('/products')
@login_required
@permission_required('products')
def products():
    p = Product.query.filter_by(company_id=cid()).all()
    return render_template('products.html', products=p)

@app.route('/product/add', methods=['POST'])
@login_required
@permission_required('products')
def add_product():
    p = Product(company_id=cid(), name=request.form.get('name'), category=request.form.get('category'),
        type=request.form.get('type', 'product'), unit=request.form.get('unit'),
        purchase_price=float(request.form.get('purchase_price') or 0), sale_price=float(request.form.get('sale_price') or 0),
        quantity=float(request.form.get('quantity') or 0), min_quantity=float(request.form.get('min_quantity') or 0),
        description=request.form.get('description'))
    db.session.add(p); db.session.commit()
    flash('تم إضافة المنتج بنجاح', 'success')
    return redirect(url_for('products'))

@app.route('/product/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('products')
def edit_product(id):
    p = db.session.get(Product, id)
    if p and p.company_id == cid():
        p.name = request.form.get('name'); p.category = request.form.get('category')
        p.type = request.form.get('type', 'product'); p.unit = request.form.get('unit')
        p.purchase_price = float(request.form.get('purchase_price') or 0)
        p.sale_price = float(request.form.get('sale_price') or 0)
        p.quantity = float(request.form.get('quantity') or 0)
        p.min_quantity = float(request.form.get('min_quantity') or 0)
        p.description = request.form.get('description'); p.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل المنتج بنجاح', 'success')
    return redirect(url_for('products'))

@app.route('/product/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('products')
def delete_product(id):
    p = db.session.get(Product, id)
    if p and p.company_id == cid(): p.status = 'deleted'; db.session.commit()
    flash('تم حذف المنتج', 'success')
    return redirect(url_for('products'))

# ==================== PURCHASES ====================

@app.route('/purchases')
@login_required
@permission_required('purchases')
def purchases():
    p = Purchase.query.filter_by(company_id=cid()).order_by(Purchase.date.desc()).all()
    s = Supplier.query.filter_by(company_id=cid(), status='active').all()
    pr = Product.query.filter_by(company_id=cid(), status='active').all()
    pj = [{'id': x.id, 'name': x.name, 'purchase_price': x.purchase_price, 'sale_price': x.sale_price, 'quantity': x.quantity} for x in pr]
    return render_template('purchases.html', purchases=p, suppliers=s, products_json=pj)

@app.route('/purchase/add', methods=['POST'])
@login_required
@permission_required('purchases')
def add_purchase():
    pur = Purchase(company_id=cid(), supplier_id=int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        total=float(request.form.get('total') or 0), paid=float(request.form.get('paid') or 0),
        payment_method=request.form.get('payment_method', 'cash'), notes=request.form.get('notes'),
        invoice_number=request.form.get('invoice_number'), created_by=current_user.id)
    db.session.add(pur); db.session.flush()
    items_data = request.form.get('items_data', '')
    if items_data:
        for item in json.loads(items_data):
            pi = PurchaseItem(purchase_id=pur.id, product_id=item.get('product_id'), product_name=item.get('product_name'),
                quantity=float(item.get('quantity', 0)), price=float(item.get('price', 0)), total=float(item.get('total', 0)))
            db.session.add(pi)
            if item.get('product_id'):
                prod = db.session.get(Product, item['product_id'])
                if prod: prod.quantity += float(item.get('quantity', 0))
    if pur.supplier_id:
        supplier = db.session.get(Supplier, pur.supplier_id)
        if supplier: supplier.balance += pur.total - pur.paid
    add_journal_entry(f'مشتريات', pur.total, 'purchase')
    db.session.commit()
    flash('تم إضافة المشتريات بنجاح', 'success')
    return redirect(url_for('purchases'))

@app.route('/purchase/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('purchases')
def delete_purchase(id):
    pur = db.session.get(Purchase, id)
    if pur and pur.company_id == cid():
        if pur.supplier_id:
            supplier = db.session.get(Supplier, pur.supplier_id)
            if supplier: supplier.balance -= pur.total - pur.paid
        db.session.delete(pur); db.session.commit()
        flash('تم حذف المشتريات', 'success')
    return redirect(url_for('purchases'))

# ==================== SALES ====================

@app.route('/sales')
@login_required
@permission_required('sales')
def sales():
    inv = SalesInvoice.query.filter_by(company_id=cid()).order_by(SalesInvoice.date.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    pr = Product.query.filter_by(company_id=cid(), status='active').all()
    pj = [{'id': x.id, 'name': x.name, 'purchase_price': x.purchase_price, 'sale_price': x.sale_price, 'quantity': x.quantity} for x in pr]
    return render_template('sales.html', invoices=inv, clients=cl, products_json=pj)

@app.route('/sale/add', methods=['POST'])
@login_required
@permission_required('sales')
def add_sale():
    inv = SalesInvoice(company_id=cid(), client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        total=float(request.form.get('total') or 0), paid=float(request.form.get('paid') or 0),
        payment_method=request.form.get('payment_method', 'cash'), notes=request.form.get('notes'),
        invoice_number=request.form.get('invoice_number'), created_by=current_user.id)
    inv.status = 'paid' if inv.paid >= inv.total else 'pending'
    db.session.add(inv); db.session.flush()
    items_data = request.form.get('items_data', '')
    if items_data:
        for item in json.loads(items_data):
            si = SalesInvoiceItem(invoice_id=inv.id, product_id=item.get('product_id'), product_name=item.get('product_name'),
                quantity=float(item.get('quantity', 0)), price=float(item.get('price', 0)), total=float(item.get('total', 0)))
            db.session.add(si)
            if item.get('product_id'):
                prod = db.session.get(Product, item['product_id'])
                if prod: prod.quantity -= float(item.get('quantity', 0))
    if inv.client_id:
        client = db.session.get(Client, inv.client_id)
        if client: client.balance += inv.total - inv.paid
    add_journal_entry(f'مبيعات', inv.total, 'sale')
    db.session.commit()
    flash('تم إضافة الفاتورة بنجاح', 'success')
    return redirect(url_for('sales'))

@app.route('/sale/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('sales')
def pay_sale(id):
    inv = db.session.get(SalesInvoice, id)
    if inv and inv.company_id == cid():
        amount = float(request.form.get('amount') or 0); inv.paid += amount
        if inv.paid >= inv.total: inv.status = 'paid'
        if inv.client_id:
            client = db.session.get(Client, inv.client_id)
            if client: client.balance -= amount
        add_journal_entry(f'دفعة مبيعات', amount, 'sale_payment')
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    return redirect(url_for('sales'))

@app.route('/sale/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('sales')
def delete_sale(id):
    inv = db.session.get(SalesInvoice, id)
    if inv and inv.company_id == cid():
        if inv.client_id:
            client = db.session.get(Client, inv.client_id)
            if client: client.balance -= inv.total - inv.paid
        db.session.delete(inv); db.session.commit()
        flash('تم حذف الفاتورة', 'success')
    return redirect(url_for('sales'))

# ==================== JOURNAL ====================

@app.route('/journal')
@login_required
@permission_required('accounting')
def journal():
    e = JournalEntry.query.filter_by(company_id=cid()).order_by(JournalEntry.date.desc()).all()
    return render_template('journal.html', entries=e)

@app.route('/journal/add', methods=['POST'])
@login_required
@permission_required('accounting')
def add_journal_manual():
    entry = JournalEntry(company_id=cid(), date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        description=request.form.get('description'), entry_type=request.form.get('entry_type', 'manual'),
        reference=request.form.get('reference'), created_by=current_user.id)
    db.session.add(entry); db.session.flush()
    lines_data = request.form.get('lines_data', '')
    if lines_data:
        for line in json.loads(lines_data):
            jl = JournalLine(entry_id=entry.id, account=line.get('account'), description=line.get('description'),
                debit=float(line.get('debit', 0)), credit=float(line.get('credit', 0)))
            db.session.add(jl)
    db.session.commit()
    flash('تم إضافة القيد بنجاح', 'success')
    return redirect(url_for('journal'))

@app.route('/journal/<int:id>')
@login_required
@permission_required('accounting')
def journal_detail(id):
    entry = db.session.get(JournalEntry, id)
    if not entry or entry.company_id != cid(): return jsonify({})
    lines = [{'account': l.account, 'debit': l.debit, 'credit': l.credit} for l in entry.lines]
    return jsonify({'description': entry.description, 'date': str(entry.date), 'lines': lines})

# ==================== REPORTS ====================

@app.route('/reports')
@login_required
@permission_required('reports')
def reports():
    c = cid()
    total_revenue = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=c).scalar() or 0
    total_expenses = db.session.query(db.func.sum(Purchase.total)).filter_by(company_id=c).scalar() or 0
    total_salaries = db.session.query(db.func.sum(Salary.net_salary)).filter_by(company_id=c).scalar() or 0
    total_suppliers_debt = db.session.query(db.func.sum(Supplier.balance)).filter_by(company_id=c).scalar() or 0
    total_clients_debt = db.session.query(db.func.sum(Client.balance)).filter_by(company_id=c).scalar() or 0
    recent_sales = SalesInvoice.query.filter_by(company_id=c).order_by(SalesInvoice.date.desc()).limit(10).all()
    recent_purchases = Purchase.query.filter_by(company_id=c).order_by(Purchase.date.desc()).limit(10).all()
    monthly_sales = db.session.query(db.func.strftime('%Y-%m', SalesInvoice.date).label('month'), db.func.sum(SalesInvoice.total).label('total')).filter_by(company_id=c).group_by('month').order_by(db.text('month desc')).limit(12).all()
    return render_template('reports.html', total_revenue=total_revenue, total_expenses=total_expenses,
        total_salaries=total_salaries, total_suppliers_debt=total_suppliers_debt,
        total_clients_debt=total_clients_debt, recent_sales=recent_sales,
        recent_purchases=recent_purchases, monthly_sales=monthly_sales)

@app.route('/reports/financial-statement')
@login_required
@permission_required('reports')
def financial_statement():
    c = cid()
    je_ids = [e.id for e in JournalEntry.query.filter_by(company_id=c).all()]
    total_debit = db.session.query(db.func.sum(JournalLine.debit)).filter(JournalLine.entry_id.in_(je_ids)).scalar() if je_ids else 0 or 0
    total_credit = db.session.query(db.func.sum(JournalLine.credit)).filter(JournalLine.entry_id.in_(je_ids)).scalar() if je_ids else 0 or 0
    accounts = db.session.query(JournalLine.account, db.func.sum(JournalLine.debit).label('total_debit'),
        db.func.sum(JournalLine.credit).label('total_credit')).join(JournalEntry).filter(JournalEntry.company_id == c).group_by(JournalLine.account).all() if je_ids else []
    return render_template('financial_statement.html', total_debit=total_debit or 0, total_credit=total_credit or 0, accounts=accounts)

# ==================== USERS & SETTINGS ====================

@app.route('/users')
@login_required
@admin_required
def users():
    u = User.query.filter_by(company_id=cid()).all()
    return render_template('users.html', users=u)

@app.route('/user/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    permissions = {p: p in request.form for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin']}
    if User.query.filter_by(company_id=cid(), username=request.form.get('username')).first():
        flash('اسم المستخدم موجود بالفعل', 'error')
        return redirect(url_for('users'))
    user = User(company_id=cid(), username=request.form.get('username'), full_name=request.form.get('full_name'),
        email=request.form.get('email'), phone=request.form.get('phone'), role=request.form.get('role', 'user'))
    user.set_password(request.form.get('password')); user.permissions = json.dumps(permissions)
    db.session.add(user); db.session.commit()
    flash('تم إضافة المستخدم بنجاح', 'success')
    return redirect(url_for('users'))

@app.route('/user/edit/<int:id>', methods=['POST'])
@login_required
@admin_required
def edit_user(id):
    user = db.session.get(User, id)
    if user and user.company_id == cid():
        user.full_name = request.form.get('full_name'); user.email = request.form.get('email')
        user.phone = request.form.get('phone'); user.role = request.form.get('role', 'user')
        user.is_active = 'is_active' in request.form
        permissions = {p: p in request.form for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin']}
        user.permissions = json.dumps(permissions)
        if request.form.get('password'): user.set_password(request.form.get('password'))
        db.session.commit()
        flash('تم تعديل المستخدم بنجاح', 'success')
    return redirect(url_for('users'))

@app.route('/user/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = db.session.get(User, id)
    if user and user.company_id == cid() and user.id != current_user.id:
        db.session.delete(user); db.session.commit()
        flash('تم حذف المستخدم', 'success')
    return redirect(url_for('users'))

@app.route('/settings')
@login_required
@admin_required
def settings():
    return render_template('settings.html', company=current_user.company, business_types=BUSINESS_TYPES)

@app.route('/settings/update', methods=['POST'])
@login_required
@admin_required
def update_settings():
    company = current_user.company
    company.name = request.form.get('name', 'شركتي'); company.phone = request.form.get('phone')
    company.email = request.form.get('email'); company.address = request.form.get('address')
    company.tax_number = request.form.get('tax_number'); company.commercial_reg = request.form.get('commercial_reg')
    company.activity = request.form.get('activity'); company.slogan = request.form.get('slogan')
    company.business_type = request.form.get('business_type', 'general')
    company.primary_color = request.form.get('primary_color', '#1a73e8')
    
    # Currency update check
    new_currency = request.form.get('currency', company.currency)
    new_rate = float(request.form.get('exchange_rate') or company.exchange_rate)
    if new_currency != company.currency or new_rate != company.exchange_rate:
        if company.currency_locked:
            flash('لا يمكن تغيير العملة أثناء فترة الاشتراك النشط. تواصل مع الإدارة.', 'error')
        else:
            company.currency = new_currency
            company.exchange_rate = new_rate
            if new_currency != 'YER':
                company.currency_locked = True
    
    db.session.commit()
    flash('تم تحديث إعدادات الشركة بنجاح', 'success')
    return redirect(url_for('settings'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if new_password != confirm_password:
        flash('كلمتا المرور غير متطابقتين', 'error')
    elif len(new_password) < 4:
        flash('كلمة المرور يجب أن تكون 4 أحرف على الأقل', 'error')
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash('تم تغيير كلمة المرور بنجاح', 'success')
    return redirect(url_for('settings'))

# ==================== CONTRACTING ====================

@app.route('/projects')
@login_required
@permission_required('projects')
def projects():
    p = Project.query.filter_by(company_id=cid()).order_by(Project.created_at.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    return render_template('projects.html', projects=p, clients=cl)

@app.route('/project/add', methods=['POST'])
@login_required
@permission_required('projects')
def add_project():
    proj = Project(company_id=cid(), name=request.form.get('name'),
        client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        contract_number=request.form.get('contract_number'),
        contract_value=float(request.form.get('contract_value') or 0),
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else date.today(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        location=request.form.get('location'), description=request.form.get('description'))
    db.session.add(proj); db.session.commit()
    flash('تم إضافة المشروع بنجاح', 'success')
    return redirect(url_for('projects'))

@app.route('/project/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('projects')
def edit_project(id):
    proj = db.session.get(Project, id)
    if proj and proj.company_id == cid():
        proj.name = request.form.get('name')
        proj.client_id = int(request.form.get('client_id')) if request.form.get('client_id') else None
        proj.contract_number = request.form.get('contract_number')
        proj.contract_value = float(request.form.get('contract_value') or 0)
        proj.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else proj.start_date
        proj.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else proj.end_date
        proj.location = request.form.get('location'); proj.description = request.form.get('description')
        proj.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل المشروع بنجاح', 'success')
    return redirect(url_for('projects'))

@app.route('/project/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('projects')
def delete_project(id):
    proj = db.session.get(Project, id)
    if proj and proj.company_id == cid(): proj.status = 'deleted'; db.session.commit()
    flash('تم حذف المشروع', 'success')
    return redirect(url_for('projects'))

@app.route('/claims')
@login_required
@permission_required('claims')
def claims():
    c = Claim.query.filter_by(company_id=cid()).order_by(Claim.date.desc()).all()
    p = Project.query.filter_by(company_id=cid(), status='active').all()
    return render_template('claims.html', claims=c, projects=p)

@app.route('/claim/add', methods=['POST'])
@login_required
@permission_required('claims')
def add_claim():
    cl = Claim(company_id=cid(), project_id=int(request.form.get('project_id')),
        claim_number=request.form.get('claim_number'),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        amount=float(request.form.get('amount') or 0),
        approved_amount=float(request.form.get('approved_amount') or 0),
        paid_amount=float(request.form.get('paid_amount') or 0),
        completion_percentage=float(request.form.get('completion_percentage') or 0),
        status=request.form.get('status', 'pending'), notes=request.form.get('notes'),
        created_by=current_user.id)
    db.session.add(cl); db.session.commit()
    flash('تم إضافة المستخلص بنجاح', 'success')
    return redirect(url_for('claims'))

@app.route('/claim/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('claims')
def pay_claim(id):
    cl = db.session.get(Claim, id)
    if cl and cl.company_id == cid():
        amount = float(request.form.get('amount') or 0); cl.paid_amount += amount
        if cl.paid_amount >= cl.approved_amount: cl.status = 'paid'
        add_journal_entry(f'دفعة مستخلص - {cl.claim_number}', amount, 'sale_payment')
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    return redirect(url_for('claims'))

@app.route('/claim/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('claims')
def delete_claim(id):
    cl = db.session.get(Claim, id)
    if cl and cl.company_id == cid(): db.session.delete(cl); db.session.commit()
    flash('تم حذف المستخلص', 'success')
    return redirect(url_for('claims'))

@app.route('/attendance')
@login_required
@permission_required('attendance')
def attendance():
    today = request.args.get('date', date.today().isoformat())
    a = DailyAttendance.query.filter_by(company_id=cid(), date=today).all()
    emps = Employee.query.filter_by(company_id=cid(), status='active').all()
    projs = Project.query.filter_by(company_id=cid(), status='active').all()
    return render_template('attendance.html', attendances=a, employees=emps, projects=projs, today=today)

@app.route('/attendance/add', methods=['POST'])
@login_required
@permission_required('attendance')
def add_attendance():
    att = DailyAttendance(company_id=cid(), employee_id=int(request.form.get('employee_id')),
        project_id=int(request.form.get('project_id')) if request.form.get('project_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        status=request.form.get('status', 'present'),
        hours=float(request.form.get('hours') or 0),
        daily_wage=float(request.form.get('daily_wage') or 0),
        notes=request.form.get('notes'))
    db.session.add(att); db.session.commit()
    flash('تم تسجيل الحضور بنجاح', 'success')
    return redirect(url_for('attendance'))

@app.route('/attendance/bulk', methods=['POST'])
@login_required
@permission_required('attendance')
def bulk_attendance():
    att_date = request.form.get('date', date.today().isoformat())
    employees = request.form.getlist('employee_ids')
    proj_id = request.form.get('project_id')
    for emp_id in employees:
        if emp_id:
            emp = db.session.get(Employee, int(emp_id))
            if emp:
                dw = emp.daily_wage if emp.wage_type == 'daily' else (emp.basic_salary / 30 if emp.basic_salary else 0)
                att = DailyAttendance(company_id=cid(), employee_id=emp.id,
                    project_id=int(proj_id) if proj_id else None,
                    date=datetime.strptime(att_date, '%Y-%m-%d').date(),
                    status='present', daily_wage=dw)
                db.session.add(att)
    db.session.commit()
    flash('تم تسجيل الحضور الجماعي بنجاح', 'success')
    return redirect(url_for('attendance', date=att_date))

@app.route('/daily-payments')
@login_required
@permission_required('daily_payments')
def daily_payments():
    dp = DailyPayment.query.filter_by(company_id=cid()).order_by(DailyPayment.date.desc()).all()
    emps = Employee.query.filter_by(company_id=cid(), status='active').all()
    projs = Project.query.filter_by(company_id=cid(), status='active').all()
    return render_template('daily_payments.html', payments=dp, employees=emps, projects=projs)

@app.route('/daily-payment/add', methods=['POST'])
@login_required
@permission_required('daily_payments')
def add_daily_payment():
    dp = DailyPayment(company_id=cid(), employee_id=int(request.form.get('employee_id')),
        project_id=int(request.form.get('project_id')) if request.form.get('project_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        amount=float(request.form.get('amount') or 0),
        payment_method=request.form.get('payment_method', 'cash'),
        notes=request.form.get('notes'))
    db.session.add(dp); add_journal_entry(f'صرف أجر يومي - {dp.employee.name}', dp.amount, 'salary')
    db.session.commit()
    flash('تم صرف الأجر بنجاح', 'success')
    return redirect(url_for('daily_payments'))

@app.route('/daily-payment/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('daily_payments')
def delete_daily_payment(id):
    dp = db.session.get(DailyPayment, id)
    if dp and dp.company_id == cid(): db.session.delete(dp); db.session.commit()
    flash('تم حذف الدفع', 'success')
    return redirect(url_for('daily_payments'))

@app.route('/materials')
@login_required
@permission_required('materials')
def materials():
    mp = MaterialPurchase.query.filter_by(company_id=cid()).order_by(MaterialPurchase.date.desc()).all()
    sup = Supplier.query.filter_by(company_id=cid(), status='active').all()
    projs = Project.query.filter_by(company_id=cid(), status='active').all()
    return render_template('materials.html', purchases=mp, suppliers=sup, projects=projs)

@app.route('/material/add', methods=['POST'])
@login_required
@permission_required('materials')
def add_material():
    mp = MaterialPurchase(company_id=cid(),
        supplier_id=int(request.form.get('supplier_id')) if request.form.get('supplier_id') else None,
        project_id=int(request.form.get('project_id')) if request.form.get('project_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        total=float(request.form.get('total') or 0), paid=float(request.form.get('paid') or 0),
        payment_method=request.form.get('payment_method', 'cash'),
        notes=request.form.get('notes'), invoice_number=request.form.get('invoice_number'),
        created_by=current_user.id)
    db.session.add(mp); db.session.flush()
    items_data = request.form.get('items_data', '')
    if items_data:
        for item in json.loads(items_data):
            mi = MaterialItem(purchase_id=mp.id, material_name=item.get('name'),
                quantity=float(item.get('quantity', 0)), unit=item.get('unit'),
                price=float(item.get('price', 0)), total=float(item.get('total', 0)))
            db.session.add(mi)
    if mp.supplier_id:
        supplier = db.session.get(Supplier, mp.supplier_id)
        if supplier: supplier.balance += mp.total - mp.paid
    add_journal_entry(f'شراء مواد', mp.total, 'purchase')
    db.session.commit()
    flash('تم إضافة شراء المواد بنجاح', 'success')
    return redirect(url_for('materials'))

@app.route('/material/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('materials')
def delete_material(id):
    mp = db.session.get(MaterialPurchase, id)
    if mp and mp.company_id == cid():
        if mp.supplier_id:
            supplier = db.session.get(Supplier, mp.supplier_id)
            if supplier: supplier.balance -= mp.total - mp.paid
        db.session.delete(mp); db.session.commit()
        flash('تم حذف شراء المواد', 'success')
    return redirect(url_for('materials'))

# ==================== RESTAURANT ====================

@app.route('/menu')
@login_required
@permission_required('menu')
def menu():
    m = MenuItem.query.filter_by(company_id=cid()).order_by(MenuItem.category, MenuItem.name).all()
    return render_template('menu.html', items=m)

@app.route('/menu/add', methods=['POST'])
@login_required
@permission_required('menu')
def add_menu_item():
    mi = MenuItem(company_id=cid(), name=request.form.get('name'), category=request.form.get('category'),
        price=float(request.form.get('price') or 0), cost=float(request.form.get('cost') or 0),
        description=request.form.get('description'))
    db.session.add(mi); db.session.commit()
    flash('تم إضافة الصنف بنجاح', 'success')
    return redirect(url_for('menu'))

@app.route('/menu/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('menu')
def edit_menu_item(id):
    mi = db.session.get(MenuItem, id)
    if mi and mi.company_id == cid():
        mi.name = request.form.get('name'); mi.category = request.form.get('category')
        mi.price = float(request.form.get('price') or 0); mi.cost = float(request.form.get('cost') or 0)
        mi.description = request.form.get('description'); mi.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل الصنف بنجاح', 'success')
    return redirect(url_for('menu'))

@app.route('/menu/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('menu')
def delete_menu_item(id):
    mi = db.session.get(MenuItem, id)
    if mi and mi.company_id == cid(): mi.status = 'deleted'; db.session.commit()
    flash('تم حذف الصنف', 'success')
    return redirect(url_for('menu'))

@app.route('/orders')
@login_required
@permission_required('orders')
def orders():
    o = TableOrder.query.filter_by(company_id=cid()).order_by(TableOrder.date.desc()).all()
    m = MenuItem.query.filter_by(company_id=cid(), status='active').all()
    mj = [{'id': x.id, 'name': x.name, 'category': x.category, 'price': x.price} for x in m]
    return render_template('orders.html', orders=o, menu_json=mj)

@app.route('/order/add', methods=['POST'])
@login_required
@permission_required('orders')
def add_order():
    order = TableOrder(company_id=cid(), table_number=request.form.get('table_number'),
        date=date.today(), total=float(request.form.get('total') or 0),
        paid=float(request.form.get('paid') or 0), notes=request.form.get('notes'))
    order.status = 'paid' if order.paid >= order.total else 'pending'
    db.session.add(order); db.session.flush()
    items_data = request.form.get('items_data', '')
    if items_data:
        for item in json.loads(items_data):
            oi = OrderItem(order_id=order.id, menu_item_id=item.get('menu_item_id'),
                item_name=item.get('item_name'), quantity=float(item.get('quantity', 1)),
                price=float(item.get('price', 0)), total=float(item.get('total', 0)))
            db.session.add(oi)
    add_journal_entry(f'طلب طاولة {order.table_number}', order.total, 'sale')
    db.session.commit()
    flash('تم إضافة الطلب بنجاح', 'success')
    return redirect(url_for('orders'))

@app.route('/order/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('orders')
def pay_order(id):
    order = db.session.get(TableOrder, id)
    if order and order.company_id == cid():
        amount = float(request.form.get('amount') or 0); order.paid += amount
        if order.paid >= order.total: order.status = 'paid'
        add_journal_entry(f'دفعة طلب', amount, 'sale_payment')
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    return redirect(url_for('orders'))

@app.route('/order/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('orders')
def delete_order(id):
    order = db.session.get(TableOrder, id)
    if order and order.company_id == cid(): db.session.delete(order); db.session.commit()
    flash('تم حذف الطلب', 'success')
    return redirect(url_for('orders'))

# ==================== SERVICE ====================

@app.route('/services')
@login_required
@permission_required('services')
def services_list():
    s = Service.query.filter_by(company_id=cid()).order_by(Service.category, Service.name).all()
    return render_template('services.html', services=s)

@app.route('/service/add', methods=['POST'])
@login_required
@permission_required('services')
def add_service():
    svc = Service(company_id=cid(), name=request.form.get('name'), category=request.form.get('category'),
        price=float(request.form.get('price') or 0), description=request.form.get('description'))
    db.session.add(svc); db.session.commit()
    flash('تم إضافة الخدمة بنجاح', 'success')
    return redirect(url_for('services_list'))

@app.route('/service/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('services')
def edit_service(id):
    svc = db.session.get(Service, id)
    if svc and svc.company_id == cid():
        svc.name = request.form.get('name'); svc.category = request.form.get('category')
        svc.price = float(request.form.get('price') or 0); svc.description = request.form.get('description')
        svc.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل الخدمة بنجاح', 'success')
    return redirect(url_for('services_list'))

@app.route('/service/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('services')
def delete_service(id):
    svc = db.session.get(Service, id)
    if svc and svc.company_id == cid(): svc.status = 'deleted'; db.session.commit()
    flash('تم حذف الخدمة', 'success')
    return redirect(url_for('services_list'))

@app.route('/service-contracts')
@login_required
@permission_required('service_contracts')
def service_contracts():
    sc = ServiceContract.query.filter_by(company_id=cid()).order_by(ServiceContract.created_at.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    return render_template('service_contracts.html', contracts=sc, clients=cl)

@app.route('/service-contract/add', methods=['POST'])
@login_required
@permission_required('service_contracts')
def add_service_contract():
    sc = ServiceContract(company_id=cid(), client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        contract_number=request.form.get('contract_number'),
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else date.today(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        amount=float(request.form.get('amount') or 0), terms=request.form.get('terms'))
    db.session.add(sc); db.session.commit()
    flash('تم إضافة العقد بنجاح', 'success')
    return redirect(url_for('service_contracts'))

@app.route('/service-contract/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('service_contracts')
def delete_service_contract(id):
    sc = db.session.get(ServiceContract, id)
    if sc and sc.company_id == cid(): db.session.delete(sc); db.session.commit()
    flash('تم حذف العقد', 'success')
    return redirect(url_for('service_contracts'))

@app.route('/service-orders')
@login_required
@permission_required('service_orders')
def service_orders():
    so = ServiceOrder.query.filter_by(company_id=cid()).order_by(ServiceOrder.date.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    sv = Service.query.filter_by(company_id=cid(), status='active').all()
    return render_template('service_orders.html', orders=so, clients=cl, services=sv)

@app.route('/service-order/add', methods=['POST'])
@login_required
@permission_required('service_orders')
def add_service_order():
    so = ServiceOrder(company_id=cid(), client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        service_id=int(request.form.get('service_id')) if request.form.get('service_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        amount=float(request.form.get('amount') or 0), paid=float(request.form.get('paid') or 0),
        status=request.form.get('status', 'pending'), notes=request.form.get('notes'),
        created_by=current_user.id)
    db.session.add(so); db.session.commit()
    flash('تم إضافة طلب الخدمة بنجاح', 'success')
    return redirect(url_for('service_orders'))

@app.route('/service-order/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('service_orders')
def pay_service_order(id):
    so = db.session.get(ServiceOrder, id)
    if so and so.company_id == cid():
        amount = float(request.form.get('amount') or 0); so.paid += amount
        if so.paid >= so.amount: so.status = 'paid'
        add_journal_entry(f'دفعة خدمة', amount, 'sale_payment')
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    return redirect(url_for('service_orders'))

@app.route('/service-order/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('service_orders')
def delete_service_order(id):
    so = db.session.get(ServiceOrder, id)
    if so and so.company_id == cid(): db.session.delete(so); db.session.commit()
    flash('تم حذف طلب الخدمة', 'success')
    return redirect(url_for('service_orders'))

# ==================== EQUIPMENT (Contracting) ====================

@app.route('/equipment')
@login_required
@permission_required('equipment')
def equipment():
    e = Equipment.query.filter_by(company_id=cid()).all()
    return render_template('equipment.html', equipment=e)

@app.route('/equipment/add', methods=['POST'])
@login_required
@permission_required('equipment')
def add_equipment():
    eq = Equipment(company_id=cid(), name=request.form.get('name'), type=request.form.get('type'),
        model=request.form.get('model'), serial_number=request.form.get('serial_number'),
        purchase_date=datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d').date() if request.form.get('purchase_date') else None,
        purchase_cost=float(request.form.get('purchase_cost') or 0), notes=request.form.get('notes'))
    db.session.add(eq); db.session.commit()
    flash('تم إضافة المعدة بنجاح', 'success')
    return redirect(url_for('equipment'))

@app.route('/equipment-maintenance')
@login_required
@permission_required('equipment_maintenance')
def equipment_maintenance():
    m = EquipmentMaintenance.query.filter_by(company_id=cid()).order_by(EquipmentMaintenance.date.desc()).all()
    e = Equipment.query.filter_by(company_id=cid(), status='active').all()
    return render_template('equipment_maintenance.html', maintenance=m, equipment=e)

@app.route('/equipment-maintenance/add', methods=['POST'])
@login_required
@permission_required('equipment_maintenance')
def add_equipment_maintenance():
    em = EquipmentMaintenance(company_id=cid(), equipment_id=int(request.form.get('equipment_id')),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        type=request.form.get('type'), cost=float(request.form.get('cost') or 0), description=request.form.get('description'))
    db.session.add(em); db.session.commit()
    flash('تم إضافة الصيانة بنجاح', 'success')
    return redirect(url_for('equipment_maintenance'))

@app.route('/fuel')
@login_required
@permission_required('fuel')
def fuel():
    f = FuelRecord.query.filter_by(company_id=cid()).order_by(FuelRecord.date.desc()).all()
    v = Vehicle.query.filter_by(company_id=cid(), status='active').all()
    return render_template('fuel.html', fuel=f, vehicles=v)

@app.route('/fuel/add', methods=['POST'])
@login_required
@permission_required('fuel')
def add_fuel():
    fr = FuelRecord(company_id=cid(), vehicle_id=int(request.form.get('vehicle_id')) if request.form.get('vehicle_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        quantity=float(request.form.get('quantity') or 0), cost=float(request.form.get('cost') or 0), notes=request.form.get('notes'))
    db.session.add(fr); db.session.commit()
    flash('تم إضافة المحروقات بنجاح', 'success')
    return redirect(url_for('fuel'))

# ==================== CLEANING ====================

@app.route('/work-sites')
@login_required
@permission_required('work_sites')
def work_sites():
    ws = WorkSite.query.filter_by(company_id=cid()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    sup = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('work_sites.html', sites=ws, clients=cl, supervisors=sup)

@app.route('/work-site/add', methods=['POST'])
@login_required
@permission_required('work_sites')
def add_work_site():
    ws = WorkSite(company_id=cid(), name=request.form.get('name'),
        client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        address=request.form.get('address'),
        supervisor_id=int(request.form.get('supervisor_id')) if request.form.get('supervisor_id') else None,
        worker_count=int(request.form.get('worker_count') or 0),
        work_hours=request.form.get('work_hours'), notes=request.form.get('notes'))
    db.session.add(ws); db.session.commit()
    flash('تم إضافة موقع العمل بنجاح', 'success')
    return redirect(url_for('work_sites'))

@app.route('/teams')
@login_required
@permission_required('teams')
def teams():
    t = Team.query.filter_by(company_id=cid()).all()
    sup = Employee.query.filter_by(company_id=cid(), status='active').all()
    ws = WorkSite.query.filter_by(company_id=cid(), status='active').all()
    return render_template('teams.html', teams=t, supervisors=sup, sites=ws)

@app.route('/team/add', methods=['POST'])
@login_required
@permission_required('teams')
def add_team():
    tm = Team(company_id=cid(), name=request.form.get('name'),
        supervisor_id=int(request.form.get('supervisor_id')) if request.form.get('supervisor_id') else None,
        site_id=int(request.form.get('site_id')) if request.form.get('site_id') else None)
    db.session.add(tm); db.session.commit()
    flash('تم إضافة الفريق بنجاح', 'success')
    return redirect(url_for('teams'))

@app.route('/team/members/<int:id>', methods=['POST'])
@login_required
@permission_required('teams')
def add_team_members(id):
    emp_ids = request.form.getlist('employee_ids')
    for eid in emp_ids:
        if eid and not TeamMember.query.filter_by(team_id=id, employee_id=int(eid)).first():
            db.session.add(TeamMember(team_id=id, employee_id=int(eid)))
    db.session.commit()
    flash('تم إضافة أعضاء الفريق', 'success')
    return redirect(url_for('teams'))

@app.route('/visits')
@login_required
@permission_required('visits')
def visits():
    v = Visit.query.filter_by(company_id=cid()).order_by(Visit.date.desc()).all()
    ws = WorkSite.query.filter_by(company_id=cid(), status='active').all()
    return render_template('visits.html', visits=v, sites=ws)

@app.route('/visit/add', methods=['POST'])
@login_required
@permission_required('visits')
def add_visit():
    vis = Visit(company_id=cid(), site_id=int(request.form.get('site_id')) if request.form.get('site_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        notes=request.form.get('notes'), rating=int(request.form.get('rating') or 0))
    db.session.add(vis); db.session.commit()
    flash('تم إضافة الزيارة بنجاح', 'success')
    return redirect(url_for('visits'))

@app.route('/supervisor-reports')
@login_required
@permission_required('supervisor_reports')
def supervisor_reports():
    r = SupervisorReport.query.filter_by(company_id=cid()).order_by(SupervisorReport.date.desc()).all()
    ws = WorkSite.query.filter_by(company_id=cid(), status='active').all()
    sup = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('supervisor_reports.html', reports=r, sites=ws, supervisors=sup)

@app.route('/supervisor-report/add', methods=['POST'])
@login_required
@permission_required('supervisor_reports')
def add_supervisor_report():
    sr = SupervisorReport(company_id=cid(), site_id=int(request.form.get('site_id')) if request.form.get('site_id') else None,
        supervisor_id=int(request.form.get('supervisor_id')) if request.form.get('supervisor_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        report=request.form.get('report'), issues=request.form.get('issues'))
    db.session.add(sr); db.session.commit()
    flash('تم إضافة التقرير بنجاح', 'success')
    return redirect(url_for('supervisor_reports'))

@app.route('/complaints')
@login_required
@permission_required('complaints')
def complaints():
    c = Complaint.query.filter_by(company_id=cid()).order_by(Complaint.date.desc()).all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    ws = WorkSite.query.filter_by(company_id=cid(), status='active').all()
    return render_template('complaints.html', complaints=c, clients=cl, sites=ws)

@app.route('/complaint/add', methods=['POST'])
@login_required
@permission_required('complaints')
def add_complaint():
    comp = Complaint(company_id=cid(), client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        site_id=int(request.form.get('site_id')) if request.form.get('site_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        description=request.form.get('description'))
    db.session.add(comp); db.session.commit()
    flash('تم إضافة الشكوى بنجاح', 'success')
    return redirect(url_for('complaints'))

@app.route('/complaint/resolve/<int:id>', methods=['POST'])
@login_required
@permission_required('complaints')
def resolve_complaint(id):
    comp = db.session.get(Complaint, id)
    if comp and comp.company_id == cid():
        comp.resolution = request.form.get('resolution')
        comp.status = 'resolved'
        db.session.commit()
        flash('تم حل الشكوى', 'success')
    return redirect(url_for('complaints'))

# ==================== HOSPITAL ====================

@app.route('/patients')
@login_required
@permission_required('patients')
def patients():
    p = Patient.query.filter_by(company_id=cid()).all()
    return render_template('patients.html', patients=p)

@app.route('/patient/add', methods=['POST'])
@login_required
@permission_required('patients')
def add_patient():
    pt = Patient(company_id=cid(), name=request.form.get('name'), phone=request.form.get('phone'),
        email=request.form.get('email'), birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get('birth_date') else None,
        gender=request.form.get('gender'), address=request.form.get('address'),
        emergency_contact=request.form.get('emergency_contact'), blood_type=request.form.get('blood_type'), notes=request.form.get('notes'))
    db.session.add(pt); db.session.commit()
    flash('تم إضافة المريض بنجاح', 'success')
    return redirect(url_for('patients'))

@app.route('/doctors')
@login_required
@permission_required('doctors')
def doctors():
    d = Doctor.query.filter_by(company_id=cid()).all()
    return render_template('doctors.html', doctors=d)

@app.route('/doctor/add', methods=['POST'])
@login_required
@permission_required('doctors')
def add_doctor():
    doc = Doctor(company_id=cid(), name=request.form.get('name'), specialty=request.form.get('specialty'),
        phone=request.form.get('phone'), email=request.form.get('email'), license_number=request.form.get('license_number'))
    db.session.add(doc); db.session.commit()
    flash('تم إضافة الطبيب بنجاح', 'success')
    return redirect(url_for('doctors'))

@app.route('/appointments')
@login_required
@permission_required('appointments')
def appointments():
    a = Appointment.query.filter_by(company_id=cid()).order_by(Appointment.date.desc()).all()
    p = Patient.query.filter_by(company_id=cid()).all()
    d = Doctor.query.filter_by(company_id=cid(), status='active').all()
    return render_template('appointments.html', appointments=a, patients=p, doctors=d)

@app.route('/appointment/add', methods=['POST'])
@login_required
@permission_required('appointments')
def add_appointment():
    ap = Appointment(company_id=cid(), patient_id=int(request.form.get('patient_id')) if request.form.get('patient_id') else None,
        doctor_id=int(request.form.get('doctor_id')) if request.form.get('doctor_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        time=request.form.get('time'), status=request.form.get('status', 'scheduled'), notes=request.form.get('notes'))
    db.session.add(ap); db.session.commit()
    flash('تم إضافة الموعد بنجاح', 'success')
    return redirect(url_for('appointments'))

@app.route('/lab')
@login_required
@permission_required('lab')
def lab():
    lt = LabTest.query.filter_by(company_id=cid()).order_by(LabTest.date.desc()).all()
    p = Patient.query.filter_by(company_id=cid()).all()
    return render_template('lab.html', tests=lt, patients=p)

@app.route('/lab/add', methods=['POST'])
@login_required
@permission_required('lab')
def add_lab_test():
    lt = LabTest(company_id=cid(), patient_id=int(request.form.get('patient_id')) if request.form.get('patient_id') else None,
        test_name=request.form.get('test_name'), date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        result=request.form.get('result'), status=request.form.get('status', 'pending'))
    db.session.add(lt); db.session.commit()
    flash('تم إضافة التحليل بنجاح', 'success')
    return redirect(url_for('lab'))

@app.route('/medicines')
@login_required
@permission_required('medicines')
def medicines():
    m = Medicine.query.filter_by(company_id=cid()).all()
    return render_template('medicines.html', medicines=m)

@app.route('/medicine/add', methods=['POST'])
@login_required
@permission_required('medicines')
def add_medicine():
    med = Medicine(company_id=cid(), name=request.form.get('name'), category=request.form.get('category'),
        price=float(request.form.get('price') or 0), quantity=float(request.form.get('quantity') or 0),
        expiry_date=datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None)
    db.session.add(med); db.session.commit()
    flash('تم إضافة الدواء بنجاح', 'success')
    return redirect(url_for('medicines'))

# ==================== SCHOOL ====================

@app.route('/students')
@login_required
@permission_required('students')
def students():
    s = Student.query.filter_by(company_id=cid()).all()
    return render_template('students.html', students=s)

@app.route('/student/add', methods=['POST'])
@login_required
@permission_required('students')
def add_student():
    st = Student(company_id=cid(), name=request.form.get('name'), student_id=request.form.get('student_id'),
        grade=request.form.get('grade'), class_name=request.form.get('class_name'),
        phone=request.form.get('phone'), parent_name=request.form.get('parent_name'),
        parent_phone=request.form.get('parent_phone'))
    db.session.add(st); db.session.commit()
    flash('تم إضافة الطالب بنجاح', 'success')
    return redirect(url_for('students'))

@app.route('/subjects')
@login_required
@permission_required('subjects')
def subjects():
    s = Subject.query.filter_by(company_id=cid()).all()
    t = Employee.query.filter_by(company_id=cid(), status='active').all()
    return render_template('subjects.html', subjects=s, teachers=t)

@app.route('/subject/add', methods=['POST'])
@login_required
@permission_required('subjects')
def add_subject():
    sub = Subject(company_id=cid(), name=request.form.get('name'), grade=request.form.get('grade'),
        teacher_id=int(request.form.get('teacher_id')) if request.form.get('teacher_id') else None)
    db.session.add(sub); db.session.commit()
    flash('تم إضافة المادة بنجاح', 'success')
    return redirect(url_for('subjects'))

@app.route('/exams')
@login_required
@permission_required('exams')
def exams():
    e = Exam.query.filter_by(company_id=cid()).order_by(Exam.date.desc()).all()
    s = Subject.query.filter_by(company_id=cid(), status='active').all()
    st = Student.query.filter_by(company_id=cid(), status='active').all()
    return render_template('exams.html', exams=e, subjects=s, students=st)

@app.route('/exam/add', methods=['POST'])
@login_required
@permission_required('exams')
def add_exam():
    ex = Exam(company_id=cid(), subject_id=int(request.form.get('subject_id')) if request.form.get('subject_id') else None,
        student_id=int(request.form.get('student_id')) if request.form.get('student_id') else None,
        score=float(request.form.get('score') or 0), max_score=float(request.form.get('max_score') or 100),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        exam_type=request.form.get('exam_type'))
    db.session.add(ex); db.session.commit()
    flash('تم إضافة الامتحان بنجاح', 'success')
    return redirect(url_for('exams'))

@app.route('/fees')
@login_required
@permission_required('fees')
def fees():
    f = Fee.query.filter_by(company_id=cid()).all()
    s = Student.query.filter_by(company_id=cid(), status='active').all()
    return render_template('fees.html', fees=f, students=s)

@app.route('/fee/add', methods=['POST'])
@login_required
@permission_required('fees')
def add_fee():
    fe = Fee(company_id=cid(), student_id=int(request.form.get('student_id')) if request.form.get('student_id') else None,
        amount=float(request.form.get('amount') or 0), paid=float(request.form.get('paid') or 0),
        due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date() if request.form.get('due_date') else None,
        status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
    db.session.add(fe); db.session.commit()
    flash('تم إضافة الرسوم بنجاح', 'success')
    return redirect(url_for('fees'))

@app.route('/fee/pay/<int:id>', methods=['POST'])
@login_required
@permission_required('fees')
def pay_fee(id):
    fe = db.session.get(Fee, id)
    if fe and fe.company_id == cid():
        amount = float(request.form.get('amount') or 0); fe.paid += amount
        if fe.paid >= fe.amount: fe.status = 'paid'
        add_journal_entry(f'رسوم طالب - {fe.student.name}', amount, 'sale_payment')
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    return redirect(url_for('fees'))

# ==================== TRANSPORT ====================

@app.route('/vehicles')
@login_required
@permission_required('vehicles')
def vehicles():
    v = Vehicle.query.filter_by(company_id=cid()).all()
    return render_template('vehicles.html', vehicles=v)

@app.route('/vehicle/add', methods=['POST'])
@login_required
@permission_required('vehicles')
def add_vehicle():
    vh = Vehicle(company_id=cid(), plate_number=request.form.get('plate_number'), type=request.form.get('type'),
        model=request.form.get('model'), year=int(request.form.get('year') or 0),
        capacity=float(request.form.get('capacity') or 0), notes=request.form.get('notes'))
    db.session.add(vh); db.session.commit()
    flash('تم إضافة المركبة بنجاح', 'success')
    return redirect(url_for('vehicles'))

@app.route('/trips')
@login_required
@permission_required('trips')
def trips():
    t = Trip.query.filter_by(company_id=cid()).order_by(Trip.date.desc()).all()
    v = Vehicle.query.filter_by(company_id=cid(), status='active').all()
    d = Employee.query.filter_by(company_id=cid(), status='active').all()
    cl = Client.query.filter_by(company_id=cid(), status='active').all()
    return render_template('trips.html', trips=t, vehicles=v, drivers=d, clients=cl)

@app.route('/trip/add', methods=['POST'])
@login_required
@permission_required('trips')
def add_trip():
    tr = Trip(company_id=cid(), vehicle_id=int(request.form.get('vehicle_id')) if request.form.get('vehicle_id') else None,
        driver_id=int(request.form.get('driver_id')) if request.form.get('driver_id') else None,
        client_id=int(request.form.get('client_id')) if request.form.get('client_id') else None,
        from_location=request.form.get('from_location'), to_location=request.form.get('to_location'),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        cost=float(request.form.get('cost') or 0), revenue=float(request.form.get('revenue') or 0),
        status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
    db.session.add(tr); db.session.commit()
    flash('تم إضافة الرحلة بنجاح', 'success')
    return redirect(url_for('trips'))

@app.route('/vehicle-maintenance')
@login_required
@permission_required('vehicle_maintenance')
def vehicle_maintenance():
    m = VehicleMaintenance.query.filter_by(company_id=cid()).order_by(VehicleMaintenance.date.desc()).all()
    v = Vehicle.query.filter_by(company_id=cid(), status='active').all()
    return render_template('vehicle_maintenance.html', maintenance=m, vehicles=v)

@app.route('/vehicle-maintenance/add', methods=['POST'])
@login_required
@permission_required('vehicle_maintenance')
def add_vehicle_maintenance():
    vm = VehicleMaintenance(company_id=cid(), vehicle_id=int(request.form.get('vehicle_id')),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        type=request.form.get('type'), cost=float(request.form.get('cost') or 0), description=request.form.get('description'))
    db.session.add(vm); db.session.commit()
    flash('تم إضافة الصيانة بنجاح', 'success')
    return redirect(url_for('vehicle_maintenance'))

# ==================== FACTORY ====================

@app.route('/production-orders')
@login_required
@permission_required('production_orders')
def production_orders():
    po = ProductionOrder.query.filter_by(company_id=cid()).order_by(ProductionOrder.start_date.desc()).all()
    return render_template('production_orders.html', orders=po)

@app.route('/production-order/add', methods=['POST'])
@login_required
@permission_required('production_orders')
def add_production_order():
    po = ProductionOrder(company_id=cid(), product_name=request.form.get('product_name'),
        quantity=float(request.form.get('quantity') or 0),
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else date.today(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
    db.session.add(po); db.session.commit()
    flash('تم إضافة أمر الإنتاج بنجاح', 'success')
    return redirect(url_for('production_orders'))

@app.route('/quality')
@login_required
@permission_required('quality')
def quality():
    qc = QualityCheck.query.filter_by(company_id=cid()).order_by(QualityCheck.date.desc()).all()
    po = ProductionOrder.query.filter_by(company_id=cid(), status='active').all()
    return render_template('quality.html', checks=qc, orders=po)

@app.route('/quality/add', methods=['POST'])
@login_required
@permission_required('quality')
def add_quality_check():
    qc = QualityCheck(company_id=cid(), production_order_id=int(request.form.get('production_order_id')) if request.form.get('production_order_id') else None,
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
        passed=request.form.get('passed') == 'on', notes=request.form.get('notes'))
    db.session.add(qc); db.session.commit()
    flash('تم إضافة فحص الجودة بنجاح', 'success')
    return redirect(url_for('quality'))

@app.route('/machines')
@login_required
@permission_required('machines')
def machines():
    m = Machine.query.filter_by(company_id=cid()).all()
    return render_template('machines.html', machines=m)

@app.route('/machine/add', methods=['POST'])
@login_required
@permission_required('machines')
def add_machine():
    mc = Machine(company_id=cid(), name=request.form.get('name'), type=request.form.get('type'),
        last_maintenance=datetime.strptime(request.form.get('last_maintenance'), '%Y-%m-%d').date() if request.form.get('last_maintenance') else None,
        notes=request.form.get('notes'))
    db.session.add(mc); db.session.commit()
    flash('تم إضافة الآلة بنجاح', 'success')
    return redirect(url_for('machines'))

# ==================== LANDING & SUBSCRIPTION ====================

@app.route('/')
def landing():
    try:
        if current_user.is_authenticated:
            if current_user.role == 'super_admin':
                return redirect(url_for('super_admin_dashboard'))
            return redirect(url_for('dashboard'))
    except Exception:
        pass
    return render_template('landing.html', plans=PLANS)

@app.route('/subscription/expired')
@login_required
def subscription_expired():
    return render_template('subscription_expired.html', company=current_user.company)

@app.route('/subscription/upgrade', methods=['GET', 'POST'])
@login_required
def subscription_upgrade():
    if request.method == 'POST':
        plan_code = request.form.get('plan_code')
        plan_info = PLANS.get(plan_code, PLANS['trial'])
        sub = current_user.company.subscription
        if not sub:
            sub = Subscription(company_id=current_user.company_id, plan_code=plan_code)
            db.session.add(sub)
        sub.plan_code = plan_code
        sub.status = 'active'
        sub.start_date = date.today()
        sub.end_date = date.today() + timedelta(days=plan_info.get('days', 30))
        sub.monthly_price = plan_info['price']
        sub.max_users = plan_info['max_users']
        sub.is_trial = (plan_code == 'trial')
        
        current_user.company.subscription_status = 'active'
        current_user.company.subscription_end = sub.end_date
        current_user.company.plan_code = plan_code
        current_user.company.is_blocked = False
        db.session.commit()
        flash('تم ترقية الباقة بنجاح!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('subscription_upgrade.html', plans=PLANS, current_plan=current_user.company.plan_code)

# ==================== SUPER ADMIN ====================

@app.route('/super-admin')
@login_required
def super_admin_dashboard():
    if current_user.role != 'super_admin':
        flash('غير مصرح لك بالوصول', 'error')
        return redirect(url_for('dashboard'))
    try:
        companies_count = Company.query.count()
        active_subs = Subscription.query.filter_by(status='active').count()
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
        recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()
        recent_companies = Company.query.order_by(Company.created_at.desc()).limit(10).all()
        blocked_companies = Company.query.filter_by(is_blocked=True).count()
    except Exception:
        companies_count = 0
        active_subs = 0
        total_revenue = 0
        recent_payments = []
        recent_companies = []
        blocked_companies = 0
    return render_template('super_admin/dashboard.html',
        companies_count=companies_count, active_subs=active_subs,
        total_revenue=total_revenue, recent_payments=recent_payments,
        recent_companies=recent_companies, blocked_companies=blocked_companies)

@app.route('/super-admin/companies')
@login_required
def super_admin_companies():
    if current_user.role != 'super_admin':
        flash('غير مصرح لك بالوصول', 'error')
        return redirect(url_for('dashboard'))
    companies = Company.query.all()
    return render_template('super_admin/companies.html', companies=companies)

@app.route('/super-admin/company/<int:id>/toggle-block', methods=['POST'])
@login_required
def super_admin_toggle_block(id):
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    company = db.session.get(Company, id)
    if company:
        company.is_blocked = not company.is_blocked
        db.session.commit()
        flash('تم تحديث حالة الشركة', 'success')
    return redirect(url_for('super_admin_companies'))

@app.route('/super-admin/payments')
@login_required
def super_admin_payments():
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('super_admin/payments.html', payments=payments)

@app.route('/super-admin/plans')
@login_required
def super_admin_plans():
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    plans = Plan.query.all()
    return render_template('super_admin/plans.html', plans=plans, system_plans=PLANS)

@app.route('/super-admin/journals')
@login_required
def super_admin_journals():
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    journals = GLJournal.query.order_by(GLJournal.date.desc()).limit(50).all()
    companies = Company.query.all()
    return render_template('super_admin/journals.html', journals=journals, companies=companies)

@app.route('/super-admin/journal/add', methods=['POST'])
@login_required
def super_admin_add_journal():
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    company_id = int(request.form.get('company_id'))
    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today()
    description = request.form.get('description', '')
    lines_json = request.form.get('lines', '[]')
    lines = json.loads(lines_json)
    
    total_debit = sum(float(l.get('debit', 0)) for l in lines)
    total_credit = sum(float(l.get('credit', 0)) for l in lines)
    
    journal = GLJournal(company_id=company_id, date=date, description=description,
                       total_debit=total_debit, total_credit=total_credit, created_by=current_user.id)
    db.session.add(journal)
    db.session.flush()
    
    for line in lines:
        gl = GLJournalLine(journal_id=journal.id, account_code=line.get('account_code', ''),
                          account_name=line.get('account_name', ''), description=line.get('description', ''),
                          debit=float(line.get('debit', 0)), credit=float(line.get('credit', 0)))
        db.session.add(gl)
    
    db.session.commit()
    flash('تم إضافة القيد المحاسبي', 'success')
    return redirect(url_for('super_admin_journals'))

@app.route('/super-admin/reports')
@login_required
def super_admin_reports():
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    companies = Company.query.all()
    total_revenue = db.session.query(db.func.sum(Payment.amount)).filter_by(status='completed').scalar() or 0
    total_companies = Company.query.count()
    active_subs = Subscription.query.filter_by(status='active').count()
    return render_template('super_admin/reports.html', companies=companies, total_revenue=total_revenue,
                          total_companies=total_companies, active_subs=active_subs)

@app.route('/super-admin/company/<int:id>/update-currency', methods=['POST'])
@login_required
def super_admin_update_currency(id):
    if current_user.role != 'super_admin':
        flash('غير مصرح', 'error')
        return redirect(url_for('dashboard'))
    company = db.session.get(Company, id)
    if company:
        company.currency = request.form.get('currency', 'YER')
        company.exchange_rate = float(request.form.get('exchange_rate') or 1.0)
        company.currency_locked = True
        db.session.commit()
        flash('تم تحديث العملة', 'success')
    return redirect(url_for('super_admin_companies'))

# ==================== ACCOUNTS ====================

@app.route('/api/employee/<int:id>')
@login_required
def api_employee(id):
    emp = db.session.get(Employee, id)
    if not emp or emp.company_id != cid():
        return jsonify({})
    return jsonify({
        'id': emp.id, 'name': emp.name, 'card_number': emp.card_number or '',
        'code': emp.code or '', 'position': emp.position or '',
        'birth_date': str(emp.birth_date) if emp.birth_date else '',
        'birth_place': emp.birth_place or '', 'join_date': str(emp.join_date) if emp.join_date else '',
        'area': emp.area or 'غير محدد', 'basic_salary': emp.basic_salary,
        'comprehensive_salary': emp.comprehensive_salary, 'daily_wage': emp.daily_wage,
        'wage_type': emp.wage_type or 'monthly', 'status': emp.status, 'notes': emp.notes or ''
    })

@app.route('/accounts')
@login_required
@permission_required('accounting')
def accounts():
    accs = Account.query.filter_by(company_id=cid(), status='active').order_by(Account.code).all()
    return render_template('accounts.html', accounts=accs)

@app.route('/account/add', methods=['POST'])
@login_required
@permission_required('accounting')
def add_account():
    acc = Account(company_id=cid(), code=request.form.get('code'), name=request.form.get('name'),
        type=request.form.get('type'), parent_id=int(request.form.get('parent_id') or 0) or None,
        description=request.form.get('description'))
    db.session.add(acc); db.session.commit()
    flash('تم إضافة الحساب بنجاح', 'success')
    return redirect(url_for('accounts'))

@app.route('/account/edit/<int:id>', methods=['POST'])
@login_required
@permission_required('accounting')
def edit_account(id):
    acc = db.session.get(Account, id)
    if acc and acc.company_id == cid():
        acc.code = request.form.get('code'); acc.name = request.form.get('name')
        acc.type = request.form.get('type'); acc.description = request.form.get('description')
        acc.status = request.form.get('status', 'active')
        db.session.commit()
        flash('تم تعديل الحساب بنجاح', 'success')
    return redirect(url_for('accounts'))

@app.route('/account/delete/<int:id>', methods=['POST'])
@login_required
@permission_required('accounting')
def delete_account(id):
    acc = db.session.get(Account, id)
    if acc and acc.company_id == cid(): acc.status = 'deleted'; db.session.commit()
    flash('تم حذف الحساب', 'success')
    return redirect(url_for('accounts'))

@app.route('/financial-dashboard')
@login_required
@permission_required('accounting')
def financial_dashboard():
    c = cid()
    accounts = Account.query.filter_by(company_id=c, status='active').order_by(Account.type, Account.code).all()
    total_cash = Account.query.filter_by(company_id=c, type='cash').with_entities(db.func.sum(Account.balance)).scalar() or 0
    total_bank = Account.query.filter_by(company_id=c, type='bank').with_entities(db.func.sum(Account.balance)).scalar() or 0
    total_receivables = Account.query.filter_by(company_id=c, type='receivables').with_entities(db.func.sum(Account.balance)).scalar() or 0
    total_payables = Account.query.filter_by(company_id=c, type='payables').with_entities(db.func.sum(Account.balance)).scalar() or 0
    return render_template('financial_dashboard.html', accounts=accounts,
        total_cash=total_cash, total_bank=total_bank,
        total_receivables=total_receivables, total_payables=total_payables)

# ==================== INIT ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        # Migration: Add missing columns to company table
        try:
            db.session.execute(db.text("ALTER TABLE company ADD COLUMN currency VARCHAR(10) DEFAULT 'YER'"))
            db.session.execute(db.text("ALTER TABLE company ADD COLUMN exchange_rate FLOAT DEFAULT 1.0"))
            db.session.execute(db.text("ALTER TABLE company ADD COLUMN currency_locked BOOLEAN DEFAULT 0"))
            db.session.commit()
        except Exception:
            db.session.rollback()  # Columns already exist
        
        # Create Super Admin company if not exists
        super_company = Company.query.filter_by(code='SUPER').first()
        if not super_company:
            super_company = Company(
                name='Al-Ghaith SaaS', code='SUPER', business_type='general',
                is_active=True, subscription_status='active', is_blocked=False,
                currency='YER', exchange_rate=1.0
            )
            db.session.add(super_company)
            db.session.flush()
        
        # Fix existing super_admin users to point to SUPER company
        sa_users = User.query.filter_by(username='superadmin').all()
        for sa in sa_users:
            if sa.company_id != super_company.id:
                sa.company_id = super_company.id
        db.session.commit()
        
        # Create Super Admin if not exists
        if not User.query.filter_by(username='superadmin').first():
            super_admin = User(
                company_id=super_company.id,
                username='superadmin',
                full_name='Super Admin',
                role='super_admin',
                is_active=True,
                permissions=json.dumps({p: True for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin','projects','claims','attendance','daily_payments','materials','menu','orders','services','service_contracts','service_orders','equipment','fuel','patients','doctors','appointments','lab','medicines','students','subjects','exams','fees','vehicles','trips','production_orders','quality','machines','work_sites','teams','visits','supervisor_reports','complaints']})
            )
            super_admin.set_password('superadmin123')
            db.session.add(super_admin)
            db.session.commit()
            print('Super Admin created: superadmin / superadmin123')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5050, debug=False)
