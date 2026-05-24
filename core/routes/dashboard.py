# core/routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from core import db
from core.models import Employee, Supplier, Client, Product, Salary, Purchase, SalesInvoice, Project, Claim, \
    DailyAttendance, MenuItem, TableOrder, Patient, Doctor, Appointment, Student, Subject, Fee, Trip, Vehicle, \
    ProductionOrder, QualityCheck, Machine, WorkSite, Visit, ClientContract, Service, ServiceOrder, \
    ServiceContract, Exam, Team
from activities.employee_transport.models import ETTrip, Bus as ETBus, Driver as ETDriver, TransportRoute as ETRoute, EmployeeAssignment as ETAssignment, Violation as ETViolation, RideLog as ETRideLog
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')  # ← تغيير المسار من '/' إلى '/dashboard'
@login_required
def index():
    company_id = current_user.company_id
    business_type = current_user.company.business_type if current_user.company else 'general'

    # المتغيرات الأساسية المشتركة
    context = {
        'business_type': business_type,
        'employees_count': Employee.query.filter_by(company_id=company_id, status='active').count(),
        'suppliers_count': Supplier.query.filter_by(company_id=company_id, status='active').count(),
        'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
        'products_count': Product.query.filter_by(company_id=company_id, status='active').count(),
    }

    # إحصائيات الرواتب
    today = date.today().strftime('%Y-%m')
    month_salaries = Salary.query.filter_by(company_id=company_id, month=today).all()
    context['total_salaries'] = sum(s.net_salary for s in month_salaries)

    # إحصائيات المشتريات والمبيعات
    context['total_purchases'] = db.session.query(db.func.sum(Purchase.total)).filter_by(
        company_id=company_id).scalar() or 0
    context['total_sales'] = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(
        company_id=company_id).scalar() or 0
    context['recent_sales'] = SalesInvoice.query.filter_by(company_id=company_id).order_by(
        SalesInvoice.date.desc()).limit(10).all()
    context['recent_purchases'] = Purchase.query.filter_by(company_id=company_id).order_by(Purchase.date.desc()).limit(
        10).all()

    # حسب نوع النشاط
    if business_type == 'contracting':
        context['projects_count'] = Project.query.filter_by(company_id=company_id, status='active').count()
        context['pending_claims'] = Claim.query.filter_by(company_id=company_id, status='pending').count()
        context['total_claims'] = db.session.query(db.func.sum(Claim.amount)).filter_by(
            company_id=company_id).scalar() or 0
        context['total_paid_claims'] = db.session.query(db.func.sum(Claim.paid_amount)).filter_by(
            company_id=company_id).scalar() or 0
        context['today_attendance'] = DailyAttendance.query.filter_by(company_id=company_id, date=date.today()).count()
        context['recent_claims'] = Claim.query.filter_by(company_id=company_id).order_by(Claim.date.desc()).limit(
            5).all()
        context['recent_projects'] = Project.query.filter_by(company_id=company_id).order_by(
            Project.created_at.desc()).limit(5).all()

    elif business_type == 'restaurant':
        context['menu_count'] = MenuItem.query.filter_by(company_id=company_id, status='active').count()
        context['today_orders'] = TableOrder.query.filter_by(company_id=company_id, date=date.today()).count()
        context['today_revenue'] = db.session.query(db.func.sum(TableOrder.total)).filter_by(company_id=company_id,
                                                                                             date=date.today()).scalar() or 0
        context['pending_orders'] = TableOrder.query.filter_by(company_id=company_id, status='pending').count()
        context['recent_orders'] = TableOrder.query.filter_by(company_id=company_id).order_by(
            TableOrder.date.desc()).limit(10).all()

    elif business_type == 'hospital':
        context['patients_count'] = Patient.query.filter_by(company_id=company_id).count()
        context['doctors_count'] = Doctor.query.filter_by(company_id=company_id, status='active').count()
        context['today_appointments'] = Appointment.query.filter_by(company_id=company_id, date=date.today()).count()
        context['pending_appointments'] = Appointment.query.filter_by(company_id=company_id, status='scheduled').count()
        context['recent_appointments'] = Appointment.query.filter_by(company_id=company_id).order_by(
            Appointment.date.desc()).limit(10).all()

    elif business_type == 'school':
        context['students_count'] = Student.query.filter_by(company_id=company_id, status='active').count()
        context['subjects_count'] = Subject.query.filter_by(company_id=company_id, status='active').count()
        context['total_fees'] = db.session.query(db.func.sum(Fee.amount)).filter_by(company_id=company_id).scalar() or 0
        context['pending_fees'] = Fee.query.filter_by(company_id=company_id, status='pending').count()
        context['recent_exams'] = Exam.query.filter_by(company_id=company_id).order_by(Exam.date.desc()).limit(10).all()

    elif business_type == 'transport':
        context['vehicles_count'] = Vehicle.query.filter_by(company_id=company_id, status='active').count()
        context['today_trips'] = Trip.query.filter_by(company_id=company_id, date=date.today()).count()
        context['total_revenue'] = db.session.query(db.func.sum(Trip.revenue)).filter_by(
            company_id=company_id).scalar() or 0
        context['pending_trips'] = Trip.query.filter_by(company_id=company_id, status='pending').count()
        context['recent_trips'] = Trip.query.filter_by(company_id=company_id).order_by(Trip.date.desc()).limit(10).all()

    elif business_type == 'factory':
        context['production_orders'] = ProductionOrder.query.filter_by(company_id=company_id).count()
        context['machines_count'] = Machine.query.filter_by(company_id=company_id, status='active').count()
        context['quality_checks'] = QualityCheck.query.filter_by(company_id=company_id).count()
        context['recent_orders'] = ProductionOrder.query.filter_by(company_id=company_id).order_by(
            ProductionOrder.start_date.desc()).limit(10).all()

    elif business_type == 'retail':
        context['products_count'] = Product.query.filter_by(company_id=company_id, status='active').count()
        context['today_sales'] = SalesInvoice.query.filter_by(company_id=company_id, date=date.today()).count()
        context['today_revenue'] = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=company_id,
                                                                                               date=date.today()).scalar() or 0
        context['low_stock'] = Product.query.filter(Product.company_id == company_id,
                                                    Product.quantity <= Product.min_quantity).count()
        context['recent_sales'] = SalesInvoice.query.filter_by(company_id=company_id).order_by(
            SalesInvoice.date.desc()).limit(10).all()
        context['recent_purchases'] = Purchase.query.filter_by(company_id=company_id).order_by(
            Purchase.date.desc()).limit(10).all()

    elif business_type == 'cleaning':
        context['clients_count'] = Client.query.filter_by(company_id=company_id, status='active').count()
        context['teams_count'] = Team.query.filter_by(company_id=company_id, status='active').count()
        context['active_contracts'] = ClientContract.query.filter_by(company_id=company_id, status='active').count()
        context['today_visits'] = Visit.query.filter_by(company_id=company_id, date=date.today()).count()
        context['recent_visits'] = Visit.query.filter_by(company_id=company_id).order_by(Visit.date.desc()).limit(
            10).all()

    elif business_type == 'employee_transport':
        context['buses_count'] = ETBus.query.filter_by(company_id=company_id, status='active').count()
        context['drivers_count'] = ETDriver.query.filter_by(company_id=company_id, status='active').count()
        context['routes_count'] = ETRoute.query.filter_by(company_id=company_id, status='active').count()
        context['assignments_count'] = ETAssignment.query.filter_by(company_id=company_id, status='active').count()
        context['today_trips'] = ETTrip.query.filter_by(company_id=company_id, date=date.today()).count()
        context['today_rides'] = ETRideLog.query.join(ETTrip).filter(
            ETTrip.company_id == company_id, ETTrip.date == date.today()).count()
        context['unresolved_violations'] = ETViolation.query.filter_by(company_id=company_id, resolved=False).count()
        context['recent_violations'] = ETViolation.query.filter_by(company_id=company_id).order_by(
            ETViolation.date.desc()).limit(5).all()

    elif business_type == 'service':
        context['services_count'] = Service.query.filter_by(company_id=company_id, status='active').count()
        context['active_contracts'] = ServiceContract.query.filter_by(company_id=company_id, status='active').count()
        context['pending_orders'] = ServiceOrder.query.filter_by(company_id=company_id, status='pending').count()
        context['total_revenue'] = db.session.query(db.func.sum(ServiceOrder.amount)).filter_by(
            company_id=company_id).scalar() or 0
        context['recent_orders'] = ServiceOrder.query.filter_by(company_id=company_id).order_by(
            ServiceOrder.date.desc()).limit(10).all()

    return render_template('dashboard.html', **context)