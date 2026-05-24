# core/routes/settings.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from helpers.constants import BUSINESS_TYPES

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    company = current_user.company

    if request.method == 'POST':
        try:
            company.name = request.form.get('name', company.name)
            company.activity = request.form.get('activity', company.activity)
            company.phone = request.form.get('phone', company.phone)
            company.email = request.form.get('email', company.email)
            company.address = request.form.get('address', company.address)
            company.tax_number = request.form.get('tax_number', company.tax_number)
            company.commercial_reg = request.form.get('commercial_reg', company.commercial_reg)
            company.slogan = request.form.get('slogan', company.slogan)
            company.business_type = request.form.get('business_type', company.business_type)
            company.primary_color = request.form.get('primary_color', company.primary_color)

            # تحديث العملة
            new_currency = request.form.get('currency', company.currency)
            new_rate = float(request.form.get('exchange_rate') or company.exchange_rate)

            if not company.currency_locked:
                company.currency = new_currency
                company.exchange_rate = new_rate
                if new_currency != 'YER':
                    company.currency_locked = True

            db.session.commit()
            flash('تم تحديث إعدادات الشركة بنجاح', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'خطأ: {str(e)}', 'error')

        return redirect(url_for('settings.settings'))

    return render_template('settings.html',
                           company=company,
                           business_types=BUSINESS_TYPES,
                           title='إعدادات الشركة')