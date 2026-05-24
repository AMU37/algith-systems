# activities/base/activity_base.py
from abc import ABC, abstractmethod
from flask import Blueprint, render_template
from flask_login import login_required, current_user

class BaseActivity(ABC):
    """الفئة الأساسية لجميع الأنشطة التجارية"""

    def __init__(self, activity_id, name, code, icon, description):
        self.activity_id = activity_id
        self.name = name
        self.code = code
        self.icon = icon
        self.description = description
        self.bp = Blueprint(code, __name__, url_prefix=f'/{code}')
        self.models = []
        self._register_routes()

    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def get_permissions(self):
        pass

    @abstractmethod
    def get_dashboard_stats(self, company_id):
        pass

    def _register_routes(self):
        @self.bp.route('/dashboard')
        @login_required
        def dashboard():
            if current_user.role == 'super_admin':
                from core.routes.super_admin import super_admin_dashboard
                return super_admin_dashboard()
            stats = self.get_dashboard_stats(current_user.company_id)
            return render_template(f'{self.code}/dashboard.html', stats=stats)

        @self.bp.route('/reports')
        @login_required
        def reports():
            return render_template(f'{self.code}/reports.html')

    def get_nav_items(self):
        return {
            'name': self.name,
            'code': self.code,
            'icon': self.icon,
            'items': [
                {'name': 'لوحة التحكم', 'url': f'/{self.code}/dashboard', 'icon': 'fa-tachometer-alt'},
                {'name': 'التقارير', 'url': f'/{self.code}/reports', 'icon': 'fa-chart-line'},
            ]
        }

    def register(self, app):
        app.register_blueprint(self.bp)
        return self
