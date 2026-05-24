# core/routes/clients.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Client, ClientContract
from datetime import datetime

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
@login_required
def clients():
    clients_list = Client.query.filter_by(company_id=current_user.company_id).all()
    return render_template('clients.html', clients=clients_list, title='العملاء')


@clients_bp.route('/add', methods=['POST'])
@login_required
def add_client():
    try:
        client = Client(
            company_id=current_user.company_id,
            name=request.form.get('name'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            email=request.form.get('email'),
            tax_number=request.form.get('tax_number'),
            notes=request.form.get('notes')
        )
        db.session.add(client)
        db.session.commit()
        flash('تم إضافة العميل بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('clients.clients'))


@clients_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_client(id):
    try:
        client = Client.query.get(id)
        if client and client.company_id == current_user.company_id:
            client.name = request.form.get('name', client.name)
            client.phone = request.form.get('phone', client.phone)
            client.address = request.form.get('address', client.address)
            client.email = request.form.get('email', client.email)
            client.tax_number = request.form.get('tax_number', client.tax_number)
            client.notes = request.form.get('notes', client.notes)
            client.status = request.form.get('status', client.status)
            db.session.commit()
            flash('تم تعديل العميل بنجاح', 'success')
        else:
            flash('العميل غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('clients.clients'))


@clients_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_client(id):
    try:
        client = Client.query.get(id)
        if client and client.company_id == current_user.company_id:
            client.status = 'deleted'
            db.session.commit()
            flash('تم حذف العميل بنجاح', 'success')
        else:
            flash('العميل غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('clients.clients'))


@clients_bp.route('/client-contracts')
@login_required
def client_contracts():
    contracts = ClientContract.query.filter_by(company_id=current_user.company_id).all()
    clients_list = Client.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('client_contracts.html', contracts=contracts, clients=clients_list, title='عقود العملاء')


@clients_bp.route('/contract/add', methods=['POST'])
@login_required
def add_client_contract():
    try:
        contract = ClientContract(
            company_id=current_user.company_id,
            client_id=int(request.form.get('client_id')),
            contract_number=request.form.get('contract_number'),
            type=request.form.get('type', 'monthly'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
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
    return redirect(url_for('clients.client_contracts'))


@clients_bp.route('/contract/delete/<int:id>', methods=['POST'])
@login_required
def delete_client_contract(id):
    try:
        contract = ClientContract.query.get(id)
        if contract and contract.company_id == current_user.company_id:
            db.session.delete(contract)
            db.session.commit()
            flash('تم حذف العقد بنجاح', 'success')
        else:
            flash('العقد غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('clients.client_contracts'))