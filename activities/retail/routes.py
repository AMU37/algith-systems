from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from core import db
from core.models import Product, Purchase, PurchaseItem, SalesInvoice, SalesInvoiceItem, Client, Supplier
from datetime import datetime, date

retail_bp = Blueprint('retail', __name__, url_prefix='/retail', template_folder='templates')

@retail_bp.route('/dashboard')
@login_required
def dashboard():
    products_count = Product.query.filter_by(company_id=current_user.company_id, status='active').count()
    today_sales = SalesInvoice.query.filter_by(company_id=current_user.company_id, date=date.today()).count()
    today_revenue = db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=current_user.company_id, date=date.today()).scalar() or 0
    low_stock = Product.query.filter(Product.company_id == current_user.company_id, Product.quantity <= Product.min_quantity).count()
    recent_sales = SalesInvoice.query.filter_by(company_id=current_user.company_id).order_by(SalesInvoice.date.desc()).limit(5).all()
    recent_purchases = Purchase.query.filter_by(company_id=current_user.company_id).order_by(Purchase.date.desc()).limit(5).all()
    return render_template('retail/dashboard.html', products_count=products_count, today_sales=today_sales, today_revenue=today_revenue, low_stock=low_stock, recent_sales=recent_sales, recent_purchases=recent_purchases)

@retail_bp.route('/products')
@login_required
def products():
    products_list = Product.query.filter_by(company_id=current_user.company_id).order_by(Product.id.desc()).all()
    return render_template('retail/products.html', products=products_list)

@retail_bp.route('/add_product', methods=['POST'])
@login_required
def add_product():
    try:
        product = Product(company_id=current_user.company_id, name=request.form.get('name'), type=request.form.get('type', 'product'), category=request.form.get('category'), unit=request.form.get('unit'), purchase_price=float(request.form.get('purchase_price', 0)), sale_price=float(request.form.get('sale_price', 0)), quantity=float(request.form.get('quantity', 0)), min_quantity=float(request.form.get('min_quantity', 0)), description=request.form.get('description'), status=request.form.get('status', 'active'))
        db.session.add(product); db.session.commit()
        flash('تم إضافة المنتج بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.products'))

@retail_bp.route('/edit_product/<int:id>', methods=['POST'])
@login_required
def edit_product(id):
    product = Product.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        product.name = request.form.get('name'); product.type = request.form.get('type', 'product')
        product.category = request.form.get('category'); product.unit = request.form.get('unit')
        product.purchase_price = float(request.form.get('purchase_price', 0))
        product.sale_price = float(request.form.get('sale_price', 0))
        product.quantity = float(request.form.get('quantity', 0))
        product.min_quantity = float(request.form.get('min_quantity', 0))
        product.description = request.form.get('description'); product.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث المنتج بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.products'))

@retail_bp.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(product); db.session.commit()
        flash('تم حذف المنتج بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.products'))

@retail_bp.route('/purchases')
@login_required
def purchases():
    purchases_list = Purchase.query.filter_by(company_id=current_user.company_id).order_by(Purchase.date.desc()).all()
    suppliers = Supplier.query.filter_by(company_id=current_user.company_id).all()
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    import json as j
    return render_template('retail/purchases.html', purchases=purchases_list, suppliers=suppliers, products=products, now=date.today().strftime('%Y-%m-%d'), products_json=j.dumps([{'id': p.id, 'name': p.name, 'price': p.purchase_price} for p in products]))

@retail_bp.route('/add_purchase', methods=['POST'])
@login_required
def add_purchase():
    try:
        purchase = Purchase(company_id=current_user.company_id, supplier_id=request.form.get('supplier_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), total=float(request.form.get('total', 0)), paid=float(request.form.get('paid', 0)), payment_method=request.form.get('payment_method', 'cash'), notes=request.form.get('notes'), invoice_number=request.form.get('invoice_number'), created_by=current_user.id)
        db.session.add(purchase); db.session.flush()
        idx = 0
        while True:
            pid = request.form.get(f'product_id_{idx}')
            if not pid: break
            item = PurchaseItem(purchase_id=purchase.id, product_id=pid, product_name=request.form.get(f'product_name_{idx}'), quantity=float(request.form.get(f'qty_{idx}', 0)), price=float(request.form.get(f'price_{idx}', 0)), total=float(request.form.get(f'total_{idx}', 0)))
            db.session.add(item); idx += 1
        db.session.commit(); flash('تم تسجيل المشتريات بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.purchases'))

@retail_bp.route('/delete_purchase/<int:id>', methods=['POST'])
@login_required
def delete_purchase(id):
    purchase = Purchase.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(purchase); db.session.commit()
        flash('تم حذف المشتريات بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.purchases'))

@retail_bp.route('/sales')
@login_required
def sales():
    invoices = SalesInvoice.query.filter_by(company_id=current_user.company_id).order_by(SalesInvoice.date.desc()).all()
    clients_list = Client.query.filter_by(company_id=current_user.company_id).all()
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    import json as j
    return render_template('retail/sales.html', invoices=invoices, clients=clients_list, products=products, now=date.today().strftime('%Y-%m-%d'), products_json=j.dumps([{'id': p.id, 'name': p.name, 'price': p.sale_price} for p in products]))

@retail_bp.route('/add_sale', methods=['POST'])
@login_required
def add_sale():
    try:
        invoice = SalesInvoice(company_id=current_user.company_id, client_id=request.form.get('client_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), total=float(request.form.get('total', 0)), paid=float(request.form.get('paid', 0)), payment_method=request.form.get('payment_method', 'cash'), notes=request.form.get('notes'), invoice_number=request.form.get('invoice_number'), status=request.form.get('status', 'pending'), created_by=current_user.id)
        db.session.add(invoice); db.session.flush()
        idx = 0
        while True:
            pid = request.form.get(f'product_id_{idx}')
            if not pid: break
            item = SalesInvoiceItem(invoice_id=invoice.id, product_id=pid, product_name=request.form.get(f'product_name_{idx}'), quantity=float(request.form.get(f'qty_{idx}', 0)), price=float(request.form.get(f'price_{idx}', 0)), total=float(request.form.get(f'total_{idx}', 0)))
            db.session.add(item); idx += 1
        db.session.commit(); flash('تم تسجيل الفاتورة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.sales'))

@retail_bp.route('/delete_sale/<int:id>', methods=['POST'])
@login_required
def delete_sale(id):
    invoice = SalesInvoice.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(invoice); db.session.commit()
        flash('تم حذف الفاتورة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('retail.sales'))
