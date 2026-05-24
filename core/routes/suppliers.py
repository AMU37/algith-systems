# core/routes/suppliers.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from core import db
from core.models import Supplier, Contract, Invoice, Purchase
from datetime import datetime, date
import json

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')


# ==================== عرض الموردين ====================
@suppliers_bp.route('/')
@login_required
def suppliers():
    company_id = current_user.company_id
    suppliers_list = Supplier.query.filter_by(company_id=company_id).order_by(Supplier.id.desc()).all()
    return render_template('suppliers.html', suppliers=suppliers_list, title='الموردين')


# ==================== إضافة مورد ====================
@suppliers_bp.route('/add', methods=['POST'])
@login_required
def add_supplier():
    try:
        supplier = Supplier(
            company_id=current_user.company_id,
            name=request.form.get('name'),
            company_name=request.form.get('company_name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            tax_number=request.form.get('tax_number'),
            balance=float(request.form.get('balance') or 0),
            notes=request.form.get('notes')
        )
        db.session.add(supplier)
        db.session.commit()
        flash('تم إضافة المورد بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.suppliers'))


# ==================== تعديل مورد ====================
@suppliers_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_supplier(id):
    try:
        supplier = Supplier.query.get(id)
        if not supplier or supplier.company_id != current_user.company_id:
            flash('المورد غير موجود', 'error')
            return redirect(url_for('suppliers.suppliers'))

        supplier.name = request.form.get('name', supplier.name)
        supplier.company_name = request.form.get('company_name', supplier.company_name)
        supplier.phone = request.form.get('phone', supplier.phone)
        supplier.email = request.form.get('email', supplier.email)
        supplier.address = request.form.get('address', supplier.address)
        supplier.tax_number = request.form.get('tax_number', supplier.tax_number)
        supplier.balance = float(request.form.get('balance') or supplier.balance)
        supplier.status = request.form.get('status', supplier.status)
        supplier.notes = request.form.get('notes', supplier.notes)

        db.session.commit()
        flash('تم تعديل المورد بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.suppliers'))


# ==================== حذف مورد ====================
@suppliers_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    try:
        supplier = Supplier.query.get(id)
        if supplier and supplier.company_id == current_user.company_id:
            supplier.status = 'deleted'
            db.session.commit()
            flash('تم حذف المورد بنجاح', 'success')
        else:
            flash('المورد غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.suppliers'))


# ==================== فواتير الموردين ====================
@suppliers_bp.route('/supplier-invoices')
@login_required
def supplier_invoices():
    company_id = current_user.company_id
    invoices = Invoice.query.filter_by(company_id=company_id).order_by(Invoice.date.desc()).all()
    suppliers = Supplier.query.filter_by(company_id=company_id, status='active').all()
    return render_template('supplier_invoices.html', invoices=invoices, suppliers=suppliers, title='فواتير الموردين')


# ==================== إضافة فاتورة مورد ====================
@suppliers_bp.route('/invoice/add', methods=['POST'])
@login_required
def add_supplier_invoice():
    try:
        amount = float(request.form.get('amount') or 0)
        paid = float(request.form.get('paid') or 0)

        invoice = Invoice(
            company_id=current_user.company_id,
            supplier_id=int(request.form.get('supplier_id')),
            invoice_number=request.form.get('invoice_number'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get(
                'date') else date.today(),
            amount=amount,
            paid=paid,
            status='paid' if paid >= amount else 'pending',
            notes=request.form.get('notes'),
            created_by=current_user.id
        )
        db.session.add(invoice)

        # تحديث رصيد المورد
        supplier = Supplier.query.get(invoice.supplier_id)
        if supplier:
            supplier.balance += amount - paid

        db.session.commit()
        flash('تم إضافة الفاتورة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.supplier_invoices'))


# ==================== حذف فاتورة مورد ====================
@suppliers_bp.route('/invoice/delete/<int:id>', methods=['POST'])
@login_required
def delete_supplier_invoice(id):
    try:
        invoice = Invoice.query.get(id)
        if invoice and invoice.company_id == current_user.company_id:
            # تحديث رصيد المورد
            supplier = Supplier.query.get(invoice.supplier_id)
            if supplier:
                supplier.balance -= (invoice.amount - invoice.paid)

            db.session.delete(invoice)
            db.session.commit()
            flash('تم حذف الفاتورة بنجاح', 'success')
        else:
            flash('الفاتورة غير موجودة', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.supplier_invoices'))


# ==================== تسديد فاتورة مورد ====================
@suppliers_bp.route('/invoice/pay/<int:id>', methods=['POST'])
@login_required
def pay_supplier_invoice(id):
    try:
        invoice = Invoice.query.get(id)
        if invoice and invoice.company_id == current_user.company_id:
            amount = float(request.form.get('amount') or 0)
            invoice.paid += amount

            if invoice.paid >= invoice.amount:
                invoice.status = 'paid'

            # تحديث رصيد المورد
            supplier = Supplier.query.get(invoice.supplier_id)
            if supplier:
                supplier.balance -= amount

            db.session.commit()
            flash('تم تسجيل الدفعة بنجاح', 'success')
        else:
            flash('الفاتورة غير موجودة', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.supplier_invoices'))


# ==================== عقود الموردين ====================
@suppliers_bp.route('/contracts')
@login_required
def supplier_contracts():
    company_id = current_user.company_id
    contracts = Contract.query.filter_by(company_id=company_id).order_by(Contract.created_at.desc()).all()
    suppliers = Supplier.query.filter_by(company_id=company_id, status='active').all()
    return render_template('supplier_contracts.html', contracts=contracts, suppliers=suppliers, title='عقود الموردين')


# ==================== إضافة عقد مورد ====================
@suppliers_bp.route('/contract/add', methods=['POST'])
@login_required
def add_supplier_contract():
    try:
        contract = Contract(
            company_id=current_user.company_id,
            supplier_id=int(request.form.get('supplier_id')),
            contract_number=request.form.get('contract_number'),
            type=request.form.get('type', 'monthly'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get(
                'start_date') else date.today(),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get(
                'end_date') else None,
            amount=float(request.form.get('amount') or 0),
            terms=request.form.get('terms'),
            status=request.form.get('status', 'active')
        )
        db.session.add(contract)
        db.session.commit()
        flash('تم إضافة العقد بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.supplier_contracts'))


# ==================== حذف عقد مورد ====================
@suppliers_bp.route('/contract/delete/<int:id>', methods=['POST'])
@login_required
def delete_supplier_contract(id):
    try:
        contract = Contract.query.get(id)
        if contract and contract.company_id == current_user.company_id:
            db.session.delete(contract)
            db.session.commit()
            flash('تم حذف العقد بنجاح', 'success')
        else:
            flash('العقد غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('suppliers.supplier_contracts'))


# ==================== مشتريات الموردين ====================
@suppliers_bp.route('/purchases/<int:id>')
@login_required
def supplier_purchases(id):
    company_id = current_user.company_id
    supplier = Supplier.query.get(id)
    if not supplier or supplier.company_id != company_id:
        flash('المورد غير موجود', 'error')
        return redirect(url_for('suppliers.suppliers'))

    purchases = Purchase.query.filter_by(company_id=company_id, supplier_id=id).order_by(Purchase.date.desc()).all()
    return render_template('supplier_purchases.html', supplier=supplier, purchases=purchases,
                           title=f'مشتريات {supplier.name}')


# ==================== API للمورد (لجلب بيانات مورد) ====================
@suppliers_bp.route('/api/<int:id>')
@login_required
def api_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier or supplier.company_id != current_user.company_id:
        return jsonify({})

    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'company_name': supplier.company_name or '',
        'phone': supplier.phone or '',
        'email': supplier.email or '',
        'address': supplier.address or '',
        'tax_number': supplier.tax_number or '',
        'balance': supplier.balance,
        'status': supplier.status,
        'notes': supplier.notes or ''
    })