# app.py - الملف الرئيسي المبسط
from core import create_app, db, login_manager
import os

# إنشاء التطبيق (جميع التسجيلات تتم داخل create_app)
app = create_app()

# دالة تحميل المستخدم
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))

# السياق العام للقوالب
@app.context_processor
def inject_globals():
    from helpers.constants import BUSINESS_TYPES, PLANS
    from flask_login import current_user
    business_type = current_user.company.business_type if current_user.is_authenticated and current_user.company else None
    from datetime import date
    company = current_user.company if current_user.is_authenticated and current_user.company else None
    return {
        'BUSINESS_TYPES': BUSINESS_TYPES,
        'PLANS': PLANS,
        'business_type': business_type,
        'company': company,
        'now': date.today().strftime('%Y-%m-%d'),
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5030, debug=True)