# core/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# تهيئة قاعدة البيانات
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config=None):
    """إنشاء تطبيق Flask مع الهيكل الجديد"""

    # الحصول على المسار المطلق للمشروع
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')  # أضف هذا السطر

    # إنشاء التطبيق مع تحديد المجلدات
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)  # أضف static_folder

    # الإعدادات الأساسية
    app.config['SECRET_KEY'] = 'alghith-saas-2026-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # إعدادات قاعدة البيانات
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        instance_path = os.path.join(base_dir, 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'alghith.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # تهيئة الملحقات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'الرجاء تسجيل الدخول أولاً'

    # تسجيل filter from_json
    @app.template_filter('from_json')
    def from_json_filter(val):
        import json
        try: return json.loads(val) if val else []
        except: return []

    # تسجيل Blueprints
    from core.routes.auth import auth_bp
    from core.routes.dashboard import dashboard_bp
    from core.routes.super_admin import super_admin_bp
    from activities import activities_bp

    # تسجيل Blueprints الإضافية
    from core.routes.employees import employees_bp
    from core.routes.suppliers import suppliers_bp
    from core.routes.clients import clients_bp
    from core.routes.products import products_bp
    from core.routes.purchases import purchases_bp
    from core.routes.sales import sales_bp
    from core.routes.accounting import accounting_bp
    from core.routes.users import users_bp
    from core.routes.settings import settings_bp
    from core.routes.equipment import equipment_bp

    app.register_blueprint(employees_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(accounting_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(equipment_bp)

    # تسجيل Blueprints الأنشطة
    from activities.contracting.routes import contracting_bp
    from activities.restaurant.routes import restaurant_bp
    from activities.retail.routes import retail_bp
    from activities.cleaning.routes import cleaning_bp
    from activities.factory.routes import factory_bp
    from activities.hospital.routes import hospital_bp
    from activities.school.routes import school_bp
    from activities.service.routes import service_bp
    from activities.transport.routes import transport_bp
    from activities.employee_transport.routes import et_bp

    app.register_blueprint(contracting_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(retail_bp)
    app.register_blueprint(cleaning_bp)
    app.register_blueprint(factory_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(school_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(transport_bp)
    app.register_blueprint(et_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(super_admin_bp, url_prefix='/super-admin')
    app.register_blueprint(activities_bp)

    # طباعة معلومات للتصحيح
    print(f"[INFO] Static folder: {app.static_folder}")
    print(f"[INFO] Static folder exists: {os.path.exists(app.static_folder)}")

    return app