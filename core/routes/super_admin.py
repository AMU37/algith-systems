# core/routes/super_admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from core import db
from core.models import Company, User, Payment, Subscription, Plan, LedgerEntry
from activities import ACTIVITIES
from helpers.constants import PLANS

super_admin_bp = Blueprint('super_admin', __name__)


@super_admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    companies_count = Company.query.count()
    active_companies = Company.query.filter_by(is_active=True, is_blocked=False).count()
    users_count = User.query.count()
    total_revenue = Payment.query.filter_by(status='completed').with_entities(db.func.sum(Payment.amount)).scalar() or 0

    return render_template('super_admin/dashboard.html',
                           companies_count=companies_count,
                           active_companies=active_companies,
                           users_count=users_count,
                           total_revenue=total_revenue)


@super_admin_bp.route('/companies')
@login_required
def companies():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    companies = Company.query.all()
    return render_template('super_admin/companies.html', companies=companies)


@super_admin_bp.route('/company/create', methods=['GET', 'POST'])
@login_required
def create_company():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        try:
            company_name = request.form.get('company_name', '').strip()
            admin_username = request.form.get('admin_username', '').strip()
            admin_password = request.form.get('admin_password', '').strip()
            business_type = request.form.get('business_type', 'general')
            plan_code = request.form.get('plan_code', 'trial')

            if not company_name:
                flash('اسم الشركة مطلوب', 'error')
                return redirect(url_for('super_admin.create_company'))

            company_count = Company.query.count()
            company_code = f"C{company_count + 1:04d}"

            company = Company(
                name=company_name,
                code=company_code,
                business_type=business_type,
                is_active=True,
                plan_code=plan_code,
                subscription_status='active'
            )
            db.session.add(company)
            db.session.flush()

            if admin_username and admin_password:
                admin = User(
                    company_id=company.id,
                    username=admin_username,
                    full_name='مدير النظام',
                    role='admin',
                    is_active=True
                )
                admin.set_password(admin_password)
                db.session.add(admin)

            from datetime import date, timedelta
            plan_info = PLANS.get(plan_code, PLANS['trial'])
            days = 14 if plan_code == 'trial' else 30

            subscription = Subscription(
                company_id=company.id,
                plan_code=plan_code,
                status='active',
                start_date=date.today(),
                end_date=date.today() + timedelta(days=days),
                monthly_price=plan_info.get('price', 0),
                max_users=plan_info.get('max_users', 1),
                is_trial=(plan_code == 'trial')
            )
            db.session.add(subscription)
            company.subscription_end = subscription.end_date

            db.session.commit()
            flash(f'تم إنشاء الشركة {company.name} بنجاح', 'success')
            return redirect(url_for('super_admin.companies'))

        except Exception as e:
            db.session.rollback()
            flash(f'خطأ: {str(e)}', 'error')
            return redirect(url_for('super_admin.create_company'))

    return render_template('super_admin/create_company.html',
                           business_types=BUSINESS_TYPES, plans=PLANS)


@super_admin_bp.route('/company/<int:id>/toggle-block', methods=['POST'])
@login_required
def toggle_block(id):
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    company = Company.query.get(id)
    if company:
        company.is_blocked = not company.is_blocked
        db.session.commit()
        flash('تم تحديث حالة الشركة', 'success')
    return redirect(url_for('super_admin.companies'))


@super_admin_bp.route('/payments')
@login_required
def payments():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    payments = Payment.query.order_by(Payment.created_at.desc()).all()
    return render_template('super_admin/payments.html', payments=payments)


@super_admin_bp.route('/journals')
@login_required
def journals():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    journals = LedgerEntry.query.order_by(LedgerEntry.created_at.desc()).limit(50).all()
    companies = Company.query.all()
    return render_template('super_admin/journals.html', journals=journals, companies=companies)


@super_admin_bp.route('/add-journal', methods=['POST'])
@login_required
def add_journal():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    try:
        company_id = request.form.get('company_id')
        description = request.form.get('description')
        date_str = request.form.get('date')
        lines_json = request.form.get('lines', '[]')

        import json
        from datetime import datetime

        lines = json.loads(lines_json)
        total_debit = sum(float(l.get('debit', 0)) for l in lines)
        total_credit = sum(float(l.get('credit', 0)) for l in lines)

        entry = LedgerEntry(
            company_id=company_id,
            description=description,
            entry_date=datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.now().date(),
            entry_number=f"ENT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            total_debit=total_debit,
            total_credit=total_credit,
            status='posted'
        )
        db.session.add(entry)
        db.session.commit()

        flash('تم إضافة القيد المحاسبي بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('super_admin.journals'))

@super_admin_bp.route('/reports')
@login_required
def reports():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    companies = Company.query.all()
    total_revenue = Payment.query.filter_by(status='completed').with_entities(db.func.sum(Payment.amount)).scalar() or 0
    total_companies = Company.query.count()
    active_subs = Subscription.query.filter_by(status='active').count()
    return render_template('super_admin/reports.html',
                           companies=companies,
                           total_revenue=total_revenue,
                           total_companies=total_companies,
                           active_subs=active_subs)


@super_admin_bp.route('/plans')
@login_required
def plans():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    plans = Plan.query.all()
    return render_template('super_admin/plans.html', plans=plans, system_plans=PLANS)


@super_admin_bp.route('/activities')
@login_required
def activities():
    if current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    return render_template('super_admin/activities.html', activities=ACTIVITIES)