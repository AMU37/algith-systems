# core/routes/auth.py - كامل
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models import Company, User, Subscription
from helpers.constants import BUSINESS_TYPES, PLANS
from datetime import date, timedelta
import json

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        try:
            print("[INFO] بدء إنشاء حساب جديد")

            company_name = request.form.get('company_name', '').strip()
            admin_username = request.form.get('admin_username', '').strip()
            admin_password = request.form.get('admin_password', '').strip()
            business_type = request.form.get('business_type', 'general')
            plan_code = request.form.get('plan_code', 'trial')

            print(f"[INFO] اسم الشركة: {company_name}")
            print(f"[INFO] اسم المستخدم: {admin_username}")

            if not company_name:
                flash('اسم الشركة مطلوب', 'error')
                return redirect(url_for('auth.setup'))

            if not admin_username:
                flash('اسم المستخدم مطلوب', 'error')
                return redirect(url_for('auth.setup'))

            if not admin_password or len(admin_password) < 4:
                flash('كلمة المرور يجب أن تكون 4 أحرف على الأقل', 'error')
                return redirect(url_for('auth.setup'))

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
            print(f"[INFO] تم إنشاء الشركة (ID: {company.id})")

            admin = User(
                company_id=company.id,
                username=admin_username,
                full_name='مدير النظام',
                role='admin',
                is_active=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.flush()
            print(f"[INFO] تم إنشاء المستخدم (ID: {admin.id})")

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
            print("[INFO] تم حفظ جميع البيانات")

            login_user(admin)
            print("[INFO] تم تسجيل الدخول")

            flash('تم إنشاء حسابك بنجاح!', 'success')
            return redirect(url_for('dashboard.index'))

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'حدث خطأ: {str(e)}', 'error')
            return redirect(url_for('auth.setup'))

    return render_template('setup.html', business_types=BUSINESS_TYPES, plans=PLANS)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("[INFO] login called")
    print(f"[INFO] method: {request.method}")

    if current_user.is_authenticated:
        if current_user.role == 'super_admin':
            return redirect(url_for('super_admin.dashboard'))
        if current_user.role == 'driver':
            return redirect(url_for('employee_transport.driver_view'))
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        print(f"[INFO] login attempt: {username}")

        user = User.query.filter_by(username=username).first()
        if user:
            print(f"[INFO] user found: {user.username}")

        if user and user.check_password(password) and user.is_active:
            login_user(user)
            print(f"[INFO] login success: {username}")
            print(f"[INFO] role: {user.role}")
            if user.role == 'super_admin':
                return redirect(url_for('super_admin.dashboard'))
            if user.role == 'driver':
                return redirect(url_for('employee_transport.driver_view'))
            return redirect(url_for('dashboard.index'))

        print(f"[INFO] login failed: {username}")
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# core/routes/auth.py (الجزء الخاص بدالة landing فقط)

@auth_bp.route('/')
def landing():
    """الصفحة الرئيسية للزوار غير المسجلين"""
    # استيراد الخطط من الملف المخصص
    from helpers.constants import PLANS

    # إذا كان المستخدم مسجلاً دخوله بالفعل، أعده إلى لوحة التحكم المناسبة
    if current_user.is_authenticated:
        if current_user.role == 'super_admin':
            return redirect(url_for('super_admin.dashboard'))
        if current_user.role == 'driver':
            return redirect(url_for('employee_transport.driver_view'))
        return redirect(url_for('dashboard.index'))

    # عرض صفحة الهبوط (landing page) مع تمرير الخطط
    return render_template('landing.html', plans=PLANS)


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not new_password or len(new_password) < 4:
        flash('كلمة المرور يجب أن تكون 4 أحرف على الأقل', 'error')
    elif new_password != confirm_password:
        flash('كلمتا المرور غير متطابقتين', 'error')
    else:
        current_user.set_password(new_password)
        db.session.commit()
        flash('تم تغيير كلمة المرور بنجاح', 'success')

    return redirect(url_for('settings.settings'))