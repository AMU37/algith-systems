# core/routes/accounting.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Account, JournalEntry, JournalLine
from datetime import datetime
import json
from core.models import SalesInvoice, Purchase, Salary, Supplier, Client

accounting_bp = Blueprint('accounting', __name__, url_prefix='/accounting')


@accounting_bp.route('/financial-dashboard')
@login_required
def financial_dashboard():
    company_id = current_user.company_id

    # حساب أرصدة الحسابات
    total_cash = Account.query.filter_by(company_id=company_id, type='cash').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_bank = Account.query.filter_by(company_id=company_id, type='bank').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_receivables = Account.query.filter_by(company_id=company_id, type='receivables').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_payables = Account.query.filter_by(company_id=company_id, type='payables').with_entities(
        db.func.sum(Account.balance)).scalar() or 0

    # قائمة الحسابات
    accounts = Account.query.filter_by(company_id=company_id, status='active').order_by(Account.code).all()

    return render_template('financial_dashboard.html',
                           total_cash=total_cash,
                           total_bank=total_bank,
                           total_receivables=total_receivables,
                           total_payables=total_payables,
                           accounts=accounts,
                           title='لوحة المالية')


@accounting_bp.route('/accounts')
@login_required
def accounts():
    accounts_list = Account.query.filter_by(company_id=current_user.company_id, status='active').order_by(
        Account.code).all()
    return render_template('accounts.html', accounts=accounts_list, title='دليل الحسابات')


@accounting_bp.route('/account/add', methods=['POST'])
@login_required
def add_account():
    try:
        account = Account(
            company_id=current_user.company_id,
            code=request.form.get('code'),
            name=request.form.get('name'),
            type=request.form.get('type'),
            parent_id=int(request.form.get('parent_id')) if request.form.get('parent_id') else None,
            description=request.form.get('description')
        )
        db.session.add(account)
        db.session.commit()
        flash('تم إضافة الحساب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('accounting.accounts'))


@accounting_bp.route('/account/edit/<int:id>', methods=['POST'])
@login_required
def edit_account(id):
    try:
        account = Account.query.get(id)
        if account and account.company_id == current_user.company_id:
            account.code = request.form.get('code', account.code)
            account.name = request.form.get('name', account.name)
            account.type = request.form.get('type', account.type)
            account.description = request.form.get('description', account.description)
            account.status = request.form.get('status', account.status)
            db.session.commit()
            flash('تم تعديل الحساب بنجاح', 'success')
        else:
            flash('الحساب غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('accounting.accounts'))


@accounting_bp.route('/account/delete/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    try:
        account = Account.query.get(id)
        if account and account.company_id == current_user.company_id:
            account.status = 'deleted'
            db.session.commit()
            flash('تم حذف الحساب بنجاح', 'success')
        else:
            flash('الحساب غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('accounting.accounts'))


@accounting_bp.route('/journal')
@login_required
def journal():
    entries = JournalEntry.query.filter_by(company_id=current_user.company_id).order_by(JournalEntry.date.desc()).all()
    return render_template('journal.html', entries=entries, title='القيود المحاسبية')


@accounting_bp.route('/journal/add', methods=['POST'])
@login_required
def add_journal_manual():
    try:
        entry = JournalEntry(
            company_id=current_user.company_id,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None,
            description=request.form.get('description'),
            entry_type='manual',
            reference=request.form.get('reference'),
            created_by=current_user.id
        )
        db.session.add(entry)
        db.session.flush()

        lines_data = request.form.get('lines_data', '[]')
        lines = json.loads(lines_data)
        for line in lines:
            journal_line = JournalLine(
                entry_id=entry.id,
                account=line.get('account'),
                description=line.get('description'),
                debit=float(line.get('debit', 0)),
                credit=float(line.get('credit', 0))
            )
            db.session.add(journal_line)

        db.session.commit()
        flash('تم إضافة القيد بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('accounting.journal'))


@accounting_bp.route('/reports')
@login_required
def reports():
    company_id = current_user.company_id

    # من الحسابات المحاسبية
    total_revenue = Account.query.filter_by(company_id=company_id, type='revenue').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_expenses = Account.query.filter_by(company_id=company_id, type='expense').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_assets = Account.query.filter_by(company_id=company_id, type='asset').with_entities(
        db.func.sum(Account.balance)).scalar() or 0
    total_liabilities = Account.query.filter_by(company_id=company_id, type='liability').with_entities(
        db.func.sum(Account.balance)).scalar() or 0

    # من المعاملات
    total_salaries = Salary.query.filter_by(company_id=company_id, is_paid=True).with_entities(
        db.func.sum(Salary.net_salary)).scalar() or 0
    total_suppliers_debt = Supplier.query.filter_by(company_id=company_id).with_entities(
        db.func.sum(Supplier.balance)).scalar() or 0
    total_clients_debt = Client.query.filter_by(company_id=company_id).with_entities(
        db.func.sum(Client.balance)).scalar() or 0

    # المبيعات الشهرية
    monthly_sales = db.session.query(
        db.func.strftime('%Y-%m', SalesInvoice.date).label('month'),
        db.func.sum(SalesInvoice.total).label('total')
    ).filter_by(company_id=company_id, status='paid').group_by('month').order_by(db.text('month desc')).limit(12).all()

    return render_template('reports.html',
                           total_revenue=total_revenue,
                           total_expenses=total_expenses,
                           total_assets=total_assets,
                           total_liabilities=total_liabilities,
                           total_salaries=total_salaries,
                           total_suppliers_debt=total_suppliers_debt,
                           total_clients_debt=total_clients_debt,
                           monthly_sales=monthly_sales,
                           title='التقارير')