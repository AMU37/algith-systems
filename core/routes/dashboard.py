# core/routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from core import db
from core.models import Employee, Supplier, Client, Product, Salary, Purchase, SalesInvoice, Project, Claim, \
    DailyAttendance, MenuItem, TableOrder, Patient, Doctor, Appointment, Student, Subject, Fee, Trip, Vehicle, \
    ProductionOrder, QualityCheck, Machine, WorkSite, Visit, ClientContract, Service, ServiceOrder, \
    ServiceContract, Exam, Team
from activities.employee_transport.models import ETTrip, Bus as ETBus, Driver as ETDriver, TransportRoute as ETRoute, \
    EmployeeAssignment as ETAssignment, Violation as ETViolation, RideLog as ETRideLog, EmployeeTransportInfo
from datetime import date, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    company_id = current_user.company_id
    business_type = current_user.company.business_type if current_user.company else 'general'
    today = date.today()

    context = {'business_type': business_type}

    # ===================== CONTRACTING =====================
    if business_type == 'contracting':
        total_claims_val = db.session.query(func.sum(Claim.amount)).filter_by(company_id=company_id).scalar() or 0
        total_paid = db.session.query(func.sum(Claim.paid_amount)).filter_by(company_id=company_id).scalar() or 0
        context.update({
            'projects_count': Project.query.filter_by(company_id=company_id, status='active').count(),
            'total_contracts': Project.query.filter_by(company_id=company_id).count(),
            'total_claims': total_claims_val,
            'total_paid_claims': total_paid,
            'pending_claims': Claim.query.filter_by(company_id=company_id, status='pending').count(),
            'today_attendance': DailyAttendance.query.filter_by(company_id=company_id, date=today).count(),
            'employees_count': Employee.query.filter_by(company_id=company_id, status='active').count(),
            'recent_claims': Claim.query.filter_by(company_id=company_id).order_by(Claim.date.desc()).limit(5).all(),
            'recent_projects': Project.query.filter_by(company_id=company_id).order_by(
                Project.created_at.desc()).limit(5).all(),
        })

    # ===================== RESTAURANT =====================
    elif business_type == 'restaurant':
        context.update({
            'menu_count': MenuItem.query.filter_by(company_id=company_id, status='active').count(),
            'today_orders': TableOrder.query.filter_by(company_id=company_id, date=today).count(),
            'today_revenue': db.session.query(func.sum(TableOrder.total)).filter_by(
                company_id=company_id, date=today).scalar() or 0,
            'pending_orders': TableOrder.query.filter_by(company_id=company_id, status='pending').count(),
            'total_orders': TableOrder.query.filter_by(company_id=company_id).count(),
            'recent_orders': TableOrder.query.filter_by(company_id=company_id).order_by(
                TableOrder.date.desc()).limit(10).all(),
        })

    # ===================== HOSPITAL =====================
    elif business_type == 'hospital':
        context.update({
            'patients_count': Patient.query.filter_by(company_id=company_id).count(),
            'doctors_count': Doctor.query.filter_by(company_id=company_id, status='active').count(),
            'today_appointments': Appointment.query.filter_by(company_id=company_id, date=today).count(),
            'pending_appointments': Appointment.query.filter_by(company_id=company_id, status='scheduled').count(),
            'completed_appointments': Appointment.query.filter_by(
                company_id=company_id, status='completed').count(),
            'recent_appointments': Appointment.query.filter_by(company_id=company_id).order_by(
                Appointment.date.desc()).limit(10).all(),
        })

    # ===================== SCHOOL =====================
    elif business_type == 'school':
        context.update({
            'students_count': Student.query.filter_by(company_id=company_id, status='active').count(),
            'subjects_count': Subject.query.filter_by(company_id=company_id, status='active').count(),
            'total_fees': db.session.query(func.sum(Fee.amount)).filter_by(company_id=company_id).scalar() or 0,
            'pending_fees': Fee.query.filter_by(company_id=company_id, status='pending').count(),
            'paid_fees': Fee.query.filter_by(company_id=company_id, status='paid').count(),
            'recent_exams': Exam.query.filter_by(company_id=company_id).order_by(Exam.date.desc()).limit(10).all(),
        })

    # ===================== TRANSPORT (old) =====================
    elif business_type == 'transport':
        week_ago = today - timedelta(days=7)
        context.update({
            'vehicles_count': Vehicle.query.filter_by(company_id=company_id, status='active').count(),
            'today_trips': Trip.query.filter_by(company_id=company_id, date=today).count(),
            'weekly_trips': Trip.query.filter(Trip.company_id == company_id, Trip.date >= week_ago).count(),
            'total_revenue': db.session.query(func.sum(Trip.revenue)).filter_by(
                company_id=company_id).scalar() or 0,
            'pending_trips': Trip.query.filter_by(company_id=company_id, status='pending').count(),
            'completed_trips': Trip.query.filter_by(company_id=company_id, status='completed').count(),
            'recent_trips': Trip.query.filter_by(company_id=company_id).order_by(Trip.date.desc()).limit(10).all(),
        })

    # ===================== FACTORY =====================
    elif business_type == 'factory':
        context.update({
            'production_orders': ProductionOrder.query.filter_by(company_id=company_id).count(),
            'machines_count': Machine.query.filter_by(company_id=company_id, status='active').count(),
            'quality_checks': QualityCheck.query.filter_by(company_id=company_id).count(),
            'completed_orders': ProductionOrder.query.filter_by(company_id=company_id, status='completed').count(),
            'pending_orders': ProductionOrder.query.filter_by(company_id=company_id, status='pending').count(),
            'employees_count': Employee.query.filter_by(company_id=company_id, status='active').count(),
            'recent_orders': ProductionOrder.query.filter_by(company_id=company_id).order_by(
                ProductionOrder.start_date.desc()).limit(10).all(),
        })

    # ===================== RETAIL =====================
    elif business_type == 'retail':
        context.update({
            'products_count': Product.query.filter_by(company_id=company_id, status='active').count(),
            'today_sales': SalesInvoice.query.filter_by(company_id=company_id, date=today).count(),
            'today_revenue': db.session.query(func.sum(SalesInvoice.total)).filter_by(
                company_id=company_id, date=today).scalar() or 0,
            'low_stock': Product.query.filter(Product.company_id == company_id,
                                              Product.quantity <= Product.min_quantity).count(),
            'total_products': Product.query.filter_by(company_id=company_id).count(),
            'recent_sales': SalesInvoice.query.filter_by(company_id=company_id).order_by(
                SalesInvoice.date.desc()).limit(10).all(),
            'recent_purchases': Purchase.query.filter_by(company_id=company_id).order_by(
                Purchase.date.desc()).limit(10).all(),
        })

    # ===================== CLEANING =====================
    elif business_type == 'cleaning':
        week_ago = today - timedelta(days=7)
        context.update({
            'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
            'teams_count': Team.query.filter_by(company_id=company_id, status='active').count(),
            'active_contracts': ClientContract.query.filter_by(company_id=company_id, status='active').count(),
            'today_visits': Visit.query.filter_by(company_id=company_id, date=today).count(),
            'weekly_visits': Visit.query.filter(Visit.company_id == company_id, Visit.date >= week_ago).count(),
            'work_sites': WorkSite.query.filter_by(company_id=company_id, status='active').count(),
            'employees_count': Employee.query.filter_by(company_id=company_id, status='active').count(),
            'recent_visits': Visit.query.filter_by(company_id=company_id).order_by(Visit.date.desc()).limit(10).all(),
        })

    # ===================== EMPLOYEE TRANSPORT =====================
    elif business_type == 'employee_transport':
        week_ago = today - timedelta(days=7)
        month_start = today.replace(day=1)
        context.update({
            'buses_count': ETBus.query.filter_by(company_id=company_id, status='active').count(),
            'drivers_count': ETDriver.query.filter_by(company_id=company_id, status='active').count(),
            'routes_count': ETRoute.query.filter_by(company_id=company_id, status='active').count(),
            'assignments_count': ETAssignment.query.filter_by(company_id=company_id, status='active').count(),
            'et_employees_count': EmployeeTransportInfo.query.filter_by(company_id=company_id).count(),
            'today_trips': ETTrip.query.filter_by(company_id=company_id, date=today).count(),
            'weekly_trips': ETTrip.query.filter(ETTrip.company_id == company_id, ETTrip.date >= week_ago).count(),
            'monthly_trips': ETTrip.query.filter(ETTrip.company_id == company_id, ETTrip.date >= month_start).count(),
            'today_rides': ETRideLog.query.join(ETTrip).filter(
                ETTrip.company_id == company_id, ETTrip.date == today).count(),
            'unresolved_violations': ETViolation.query.filter_by(company_id=company_id, resolved=False).count(),
            'total_violations': ETViolation.query.filter_by(company_id=company_id).count(),
            'active_drivers_today': ETTrip.query.filter(
                ETTrip.company_id == company_id, ETTrip.date == today,
                ETTrip.status.in_(['in_progress', 'scheduled'])
            ).distinct(ETTrip.driver_id).count(),
            'recent_violations': ETViolation.query.filter_by(company_id=company_id).order_by(
                ETViolation.date.desc()).limit(5).all(),
        })

    # ===================== SERVICE =====================
    elif business_type == 'service':
        context.update({
            'services_count': Service.query.filter_by(company_id=company_id, status='active').count(),
            'active_contracts': ServiceContract.query.filter_by(company_id=company_id, status='active').count(),
            'pending_orders': ServiceOrder.query.filter_by(company_id=company_id, status='pending').count(),
            'completed_orders': ServiceOrder.query.filter_by(company_id=company_id, status='completed').count(),
            'total_revenue': db.session.query(func.sum(ServiceOrder.amount)).filter_by(
                company_id=company_id).scalar() or 0,
            'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
            'recent_orders': ServiceOrder.query.filter_by(company_id=company_id).order_by(
                ServiceOrder.date.desc()).limit(10).all(),
        })

    # ===================== TRADING =====================
    elif business_type == 'trading':
        context.update({
            'total_purchases': db.session.query(func.sum(Purchase.total)).filter_by(
                company_id=company_id).scalar() or 0,
            'total_sales': db.session.query(func.sum(SalesInvoice.total)).filter_by(
                company_id=company_id).scalar() or 0,
            'suppliers_count': Supplier.query.filter_by(company_id=company_id, status='active').count(),
            'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
            'products_count': Product.query.filter_by(company_id=company_id, status='active').count(),
            'recent_sales': SalesInvoice.query.filter_by(company_id=company_id).order_by(
                SalesInvoice.date.desc()).limit(10).all(),
            'recent_purchases': Purchase.query.filter_by(company_id=company_id).order_by(
                Purchase.date.desc()).limit(10).all(),
        })

    # ===================== GENERAL =====================
    else:
        context.update({
            'employees_count': Employee.query.filter_by(company_id=company_id, status='active').count(),
            'suppliers_count': Supplier.query.filter_by(company_id=company_id, status='active').count(),
            'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
            'products_count': Product.query.filter_by(company_id=company_id, status='active').count(),
            'total_salaries': sum(s.net_salary for s in Salary.query.filter_by(
                company_id=company_id, month=today.strftime('%Y-%m')).all()),
            'total_purchases': db.session.query(func.sum(Purchase.total)).filter_by(
                company_id=company_id).scalar() or 0,
            'total_sales': db.session.query(func.sum(SalesInvoice.total)).filter_by(
                company_id=company_id).scalar() or 0,
        })

    return render_template('dashboard.html', **context)