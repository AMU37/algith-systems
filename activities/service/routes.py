from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Service, ServiceContract, ServiceOrder, Client
from datetime import datetime, date

service_bp = Blueprint('service', __name__, url_prefix='/service', template_folder='templates')

@service_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('service/dashboard.html', services_count=Service.query.filter_by(company_id=current_user.company_id, status='active').count(), active_contracts=ServiceContract.query.filter_by(company_id=current_user.company_id, status='active').count(), pending_orders=ServiceOrder.query.filter_by(company_id=current_user.company_id, status='pending').count(), total_revenue=db.session.query(db.func.sum(ServiceOrder.amount)).filter_by(company_id=current_user.company_id).scalar() or 0, recent_orders=ServiceOrder.query.filter_by(company_id=current_user.company_id).order_by(ServiceOrder.date.desc()).limit(10).all())

@service_bp.route('/services')
@login_required
def services():
    services_list = Service.query.filter_by(company_id=current_user.company_id).all()
    return render_template('service/services.html', services=services_list)

@service_bp.route('/add_service', methods=['POST'])
@login_required
def add_service():
    try:
        srv = Service(company_id=current_user.company_id, name=request.form.get('name'), category=request.form.get('category'), price=float(request.form.get('price', 0)), description=request.form.get('description'), status=request.form.get('status', 'active'))
        db.session.add(srv); db.session.commit()
        flash('تم إضافة الخدمة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.services'))

@service_bp.route('/edit_service/<int:id>', methods=['POST'])
@login_required
def edit_service(id):
    srv = Service.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        srv.name = request.form.get('name'); srv.category = request.form.get('category')
        srv.price = float(request.form.get('price', 0)); srv.description = request.form.get('description')
        srv.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث الخدمة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.services'))

@service_bp.route('/delete_service/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    srv = Service.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(srv); db.session.commit()
        flash('تم حذف الخدمة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.services'))

@service_bp.route('/contracts')
@login_required
def contracts():
    contracts_list = ServiceContract.query.filter_by(company_id=current_user.company_id).order_by(ServiceContract.id.desc()).all()
    clients_list = Client.query.filter_by(company_id=current_user.company_id).all()
    return render_template('service/service_contracts.html', contracts=contracts_list, clients=clients_list, now=date.today().strftime('%Y-%m-%d'))

@service_bp.route('/add_service_contract', methods=['POST'])
@login_required
def add_service_contract():
    try:
        contract = ServiceContract(company_id=current_user.company_id, client_id=request.form.get('client_id') or None, contract_number=request.form.get('contract_number'), start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None, end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None, amount=float(request.form.get('amount', 0)), terms=request.form.get('terms'), status=request.form.get('status', 'active'))
        db.session.add(contract); db.session.commit()
        flash('تم إضافة العقد بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.contracts'))

@service_bp.route('/delete_service_contract/<int:id>', methods=['POST'])
@login_required
def delete_service_contract(id):
    contract = ServiceContract.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(contract); db.session.commit()
        flash('تم حذف العقد بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.contracts'))

@service_bp.route('/orders')
@login_required
def orders():
    orders_list = ServiceOrder.query.filter_by(company_id=current_user.company_id).order_by(ServiceOrder.date.desc()).all()
    clients_list = Client.query.filter_by(company_id=current_user.company_id).all()
    services_list = Service.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('service/service_orders.html', orders=orders_list, clients=clients_list, services=services_list, now=date.today().strftime('%Y-%m-%d'))

@service_bp.route('/add_service_order', methods=['POST'])
@login_required
def add_service_order():
    try:
        order = ServiceOrder(company_id=current_user.company_id, client_id=request.form.get('client_id') or None, service_id=request.form.get('service_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), amount=float(request.form.get('amount', 0)), paid=float(request.form.get('paid', 0)), status=request.form.get('status', 'pending'), notes=request.form.get('notes'), created_by=current_user.id)
        db.session.add(order); db.session.commit()
        flash('تم إضافة الطلب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.orders'))

@service_bp.route('/pay_service_order/<int:id>', methods=['POST'])
@login_required
def pay_service_order(id):
    order = ServiceOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        extra = float(request.form.get('amount', 0))
        order.paid = (order.paid or 0) + extra
        if order.paid >= order.amount: order.status = 'paid'
        else: order.status = 'partial'
        db.session.commit(); flash('تم تسجيل الدفع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.orders'))

@service_bp.route('/delete_service_order/<int:id>', methods=['POST'])
@login_required
def delete_service_order(id):
    order = ServiceOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(order); db.session.commit()
        flash('تم حذف الطلب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('service.orders'))
