from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core.models.user import User
from core import db
import json

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
@login_required
def users():
    if current_user.role != 'admin' and current_user.role != 'super_admin':
        return redirect(url_for('dashboard.index'))

    # جلب جميع المستخدمين من نفس الشركة
    all_users = User.query.filter_by(company_id=current_user.company_id).all()
    return render_template('users.html', title='المستخدمين', users=all_users)


# دالة إضافة مستخدم جديد
@users_bp.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin' and current_user.role != 'super_admin':
        flash('غير مصرح لك بهذه العملية', 'danger')
        return redirect(url_for('users.users'))

    try:
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role', 'user')

        # التحقق من وجود المستخدم في نفس الشركة
        existing_user = User.query.filter_by(
            company_id=current_user.company_id,
            username=username
        ).first()

        if existing_user:
            flash('اسم المستخدم موجود مسبقاً في شركتك', 'danger')
            return redirect(url_for('users.users'))

        # إنشاء مستخدم جديد
        new_user = User(
            company_id=current_user.company_id,
            username=username,
            full_name=full_name,
            email=email,
            phone=phone,
            role=role,
            is_active=True
        )
        new_user.set_password(password)

        # حفظ الصلاحيات (permissions)
        permissions = {
            'employees': 'employees' in request.form,
            'salaries': 'salaries' in request.form,
            'suppliers': 'suppliers' in request.form,
            'clients': 'clients' in request.form,
            'products': 'products' in request.form,
            'purchases': 'purchases' in request.form,
            'sales': 'sales' in request.form,
            'accounting': 'accounting' in request.form,
            'reports': 'reports' in request.form,
            'areas': 'areas' in request.form
        }
        new_user.permissions = json.dumps(permissions)

        db.session.add(new_user)
        db.session.commit()

        flash('تم إضافة المستخدم بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('users.users'))


# دالة حذف مستخدم
@users_bp.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if current_user.role != 'admin' and current_user.role != 'super_admin':
        flash('غير مصرح لك بهذه العملية', 'danger')
        return redirect(url_for('users.users'))

    user = User.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()

    # منع حذف المستخدم الحالي
    if user.id == current_user.id:
        flash('لا يمكنك حذف حسابك الخاص', 'danger')
        return redirect(url_for('users.users'))

    try:
        db.session.delete(user)
        db.session.commit()
        flash('تم حذف المستخدم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('users.users'))


# دالة تعديل مستخدم
@users_bp.route('/edit_user/<int:id>', methods=['POST'])
@login_required
def edit_user(id):
    if current_user.role != 'admin' and current_user.role != 'super_admin':
        flash('غير مصرح لك بهذه العملية', 'danger')
        return redirect(url_for('users.users'))

    user = User.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()

    try:
        # تحديث كلمة المرور إذا تم إدخالها
        new_password = request.form.get('password')
        if new_password and new_password.strip():
            user.set_password(new_password)

        # تحديث البيانات الأخرى
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.role = request.form.get('role')
        user.is_active = 'is_active' in request.form

        # تحديث الصلاحيات
        permissions = {
            'employees': 'employees' in request.form,
            'salaries': 'salaries' in request.form,
            'suppliers': 'suppliers' in request.form,
            'clients': 'clients' in request.form,
            'products': 'products' in request.form,
            'purchases': 'purchases' in request.form,
            'sales': 'sales' in request.form,
            'accounting': 'accounting' in request.form,
            'reports': 'reports' in request.form,
            'areas': 'areas' in request.form
        }
        user.permissions = json.dumps(permissions)

        db.session.commit()
        flash('تم تحديث المستخدم بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')

    return redirect(url_for('users.users'))