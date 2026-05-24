from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from core import db
from core.models import MenuItem, TableOrder, OrderItem
from datetime import datetime, date

restaurant_bp = Blueprint('restaurant', __name__, url_prefix='/restaurant', template_folder='templates')

@restaurant_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('restaurant/dashboard.html',
        menu_count=MenuItem.query.filter_by(company_id=current_user.company_id, status='active').count(),
        today_orders=TableOrder.query.filter_by(company_id=current_user.company_id, date=date.today()).count(),
        today_revenue=db.session.query(db.func.sum(TableOrder.total)).filter_by(company_id=current_user.company_id, date=date.today()).scalar() or 0,
        pending_orders=TableOrder.query.filter_by(company_id=current_user.company_id, status='pending').count(),
        recent_orders=TableOrder.query.filter_by(company_id=current_user.company_id).order_by(TableOrder.date.desc()).limit(10).all())

@restaurant_bp.route('/menu')
@login_required
def menu():
    items = MenuItem.query.filter_by(company_id=current_user.company_id).order_by(MenuItem.id.desc()).all()
    return render_template('restaurant/menu.html', items=items)

@restaurant_bp.route('/add_menu_item', methods=['POST'])
@login_required
def add_menu_item():
    try:
        item = MenuItem(company_id=current_user.company_id, name=request.form.get('name'), category=request.form.get('category'), price=float(request.form.get('price', 0)), cost=float(request.form.get('cost', 0)), description=request.form.get('description'), status=request.form.get('status', 'active'))
        db.session.add(item); db.session.commit()
        flash('تم إضافة الصنف بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.menu'))

@restaurant_bp.route('/edit_menu_item/<int:id>', methods=['POST'])
@login_required
def edit_menu_item(id):
    item = MenuItem.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        item.name = request.form.get('name'); item.category = request.form.get('category')
        item.price = float(request.form.get('price', 0)); item.cost = float(request.form.get('cost', 0))
        item.description = request.form.get('description'); item.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث الصنف بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.menu'))

@restaurant_bp.route('/delete_menu_item/<int:id>', methods=['POST'])
@login_required
def delete_menu_item(id):
    item = MenuItem.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(item); db.session.commit()
        flash('تم حذف الصنف بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.menu'))

@restaurant_bp.route('/orders')
@login_required
def orders():
    orders_list = TableOrder.query.filter_by(company_id=current_user.company_id).order_by(TableOrder.id.desc()).all()
    items = MenuItem.query.filter_by(company_id=current_user.company_id, status='active').all()
    import json as j
    return render_template('restaurant/orders.html', orders=orders_list, items=items, now=date.today().strftime('%Y-%m-%d'), menu_json=j.dumps([{'id': i.id, 'name': i.name, 'price': i.price} for i in items]))

@restaurant_bp.route('/add_order', methods=['POST'])
@login_required
def add_order():
    try:
        order = TableOrder(company_id=current_user.company_id, table_number=request.form.get('table_number'), total=float(request.form.get('total', 0)), paid=float(request.form.get('paid', 0)), status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
        db.session.add(order); db.session.flush()
        idx = 0
        while True:
            mid = request.form.get(f'item_id_{idx}')
            if not mid: break
            qty = float(request.form.get(f'item_qty_{idx}', 1))
            price = float(request.form.get(f'item_price_{idx}', 0))
            db.session.add(OrderItem(order_id=order.id, menu_item_id=mid, quantity=qty, price=price, total=qty * price))
            idx += 1
        db.session.commit(); flash('تم إضافة الطلب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.orders'))

@restaurant_bp.route('/pay_order/<int:id>', methods=['POST'])
@login_required
def pay_order(id):
    order = TableOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        extra = float(request.form.get('amount', 0))
        order.paid = (order.paid or 0) + extra
        if order.paid >= order.total: order.status = 'paid'
        else: order.status = 'partial'
        db.session.commit(); flash('تم تسجيل الدفع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.orders'))

@restaurant_bp.route('/delete_order/<int:id>', methods=['POST'])
@login_required
def delete_order(id):
    order = TableOrder.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(order); db.session.commit()
        flash('تم حذف الطلب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('restaurant.orders'))
