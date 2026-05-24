# activities/__init__.py
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

ACTIVITIES = {}

def register_activity(activity):
    ACTIVITIES[activity.code] = activity
    return activity

# استيراد وتسجيل جميع الأنشطة
activity_modules = [
    ('contracting', 'نشاط المقاولات'),
    ('retail', 'نشاط التجزئة'),
    ('restaurant', 'نشاط المطاعم'),
    ('cleaning', 'نشاط النظافة'),
    ('factory', 'نشاط المصنع'),
    ('hospital', 'نشاط المستشفى'),
    ('school', 'نشاط المدرسة'),
    ('service', 'نشاط الخدمات'),
    ('transport', 'نشاط النقل'),
]

for module_name, label in activity_modules:
    try:
        mod = __import__(f'activities.{module_name}', fromlist=[module_name])
        activity = getattr(mod, module_name)
        register_activity(activity)
    except ImportError:
        print(f"[WARN] {label} غير موجود")

def get_activity(activity_code):
    return ACTIVITIES.get(activity_code)

def get_activity_by_business_type(business_type):
    return ACTIVITIES.get(business_type)

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/switch/<activity_code>')
@login_required
def switch_activity(activity_code):
    activity = get_activity(activity_code)
    if activity:
        current_user.company.business_type = activity_code
        from core import db
        db.session.commit()
        return redirect(url_for(f'{activity_code}.dashboard'))
    return redirect(url_for('dashboard.index'))