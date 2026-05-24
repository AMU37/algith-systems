from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import ProductionOrder, QualityCheck, Machine
from datetime import datetime, date

factory_bp = Blueprint('factory', __name__, url_prefix='/factory', template_folder='templates')

@factory_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('factory/dashboard.html', production_orders=ProductionOrder.query.filter_by(company_id=current_user.company_id).count(), machines_count=Machine.query.filter_by(company_id=current_user.company_id, status='active').count(), quality_checks=QualityCheck.query.filter_by(company_id=current_user.company_id).count(), recent_orders=ProductionOrder.query.filter_by(company_id=current_user.company_id).order_by(ProductionOrder.start_date.desc()).limit(10).all(), employees_count=0)

@factory_bp.route('/production-orders')
@login_required
def production_orders():
    orders = ProductionOrder.query.filter_by(company_id=current_user.company_id).order_by(ProductionOrder.id.desc()).all()
    return render_template('factory/production_orders.html', orders=orders, now=date.today().strftime('%Y-%m-%d'))

@factory_bp.route('/add_production_order', methods=['POST'])
@login_required
def add_production_order():
    try:
        order = ProductionOrder(company_id=current_user.company_id, product_name=request.form.get('product_name'), quantity=float(request.form.get('quantity', 0)), start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None, end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None, status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
        db.session.add(order); db.session.commit()
        flash('تم إضافة أمر الإنتاج بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.production_orders'))

@factory_bp.route('/edit_production_order/<int:id>', methods=['POST'])
@login_required
def edit_production_order(id):
    order = ProductionOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        order.product_name = request.form.get('product_name'); order.quantity = float(request.form.get('quantity', 0))
        order.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
        order.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None
        order.status = request.form.get('status', 'pending'); order.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث أمر الإنتاج بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.production_orders'))

@factory_bp.route('/delete_production_order/<int:id>', methods=['POST'])
@login_required
def delete_production_order(id):
    order = ProductionOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(order); db.session.commit()
        flash('تم حذف أمر الإنتاج بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.production_orders'))

@factory_bp.route('/machines')
@login_required
def machines():
    machines_list = Machine.query.filter_by(company_id=current_user.company_id).all()
    return render_template('factory/machines.html', machines=machines_list)

@factory_bp.route('/add_machine', methods=['POST'])
@login_required
def add_machine():
    try:
        machine = Machine(company_id=current_user.company_id, name=request.form.get('name'), type=request.form.get('type'), status=request.form.get('status', 'active'), last_maintenance=datetime.strptime(request.form.get('last_maintenance'), '%Y-%m-%d').date() if request.form.get('last_maintenance') else None, notes=request.form.get('notes'))
        db.session.add(machine); db.session.commit()
        flash('تم إضافة الآلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.machines'))

@factory_bp.route('/edit_machine/<int:id>', methods=['POST'])
@login_required
def edit_machine(id):
    machine = Machine.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        machine.name = request.form.get('name'); machine.type = request.form.get('type')
        machine.status = request.form.get('status', 'active')
        machine.last_maintenance = datetime.strptime(request.form.get('last_maintenance'), '%Y-%m-%d').date() if request.form.get('last_maintenance') else None
        machine.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث الآلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.machines'))

@factory_bp.route('/delete_machine/<int:id>', methods=['POST'])
@login_required
def delete_machine(id):
    machine = Machine.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(machine); db.session.commit()
        flash('تم حذف الآلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.machines'))

@factory_bp.route('/quality')
@login_required
def quality():
    checks = QualityCheck.query.filter_by(company_id=current_user.company_id).order_by(QualityCheck.date.desc()).all()
    orders = ProductionOrder.query.filter_by(company_id=current_user.company_id).all()
    return render_template('factory/quality.html', checks=checks, orders=orders, now=date.today().strftime('%Y-%m-%d'))

@factory_bp.route('/add_quality_check', methods=['POST'])
@login_required
def add_quality_check():
    try:
        check = QualityCheck(company_id=current_user.company_id, production_order_id=request.form.get('production_order_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), passed=request.form.get('passed') == 'on', notes=request.form.get('notes'))
        db.session.add(check); db.session.commit()
        flash('تم إضافة فحص الجودة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.quality'))

@factory_bp.route('/delete_quality_check/<int:id>', methods=['POST'])
@login_required
def delete_quality_check(id):
    check = QualityCheck.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(check); db.session.commit()
        flash('تم حذف فحص الجودة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('factory.quality'))
