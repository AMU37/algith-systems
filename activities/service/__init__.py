from ..base.activity_base import BaseActivity

class ServiceActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=8,
            name='شركة خدمات',
            code='service',
            icon='fa-briefcase',
            description='إدارة الخدمات والعقود والطلبات'
        )

    def get_models(self):
        from .models import Service, ServiceContract, ServiceOrder
        return [Service, ServiceContract, ServiceOrder]

    def get_permissions(self):
        return [
            {'code': 'services', 'name': 'الخدمات', 'default': False},
            {'code': 'contracts', 'name': 'العقود', 'default': False},
            {'code': 'orders', 'name': 'الطلبات', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import Service, ServiceContract, ServiceOrder
        return {
            'services_count': Service.query.filter_by(company_id=company_id, status='active').count(),
            'active_contracts': ServiceContract.query.filter_by(company_id=company_id, status='active').count(),
            'total_revenue': db.session.query(db.func.sum(ServiceOrder.amount)).filter_by(company_id=company_id).scalar() or 0,
            'pending_orders': ServiceOrder.query.filter_by(company_id=company_id, status='pending').count(),
            'recent_orders': ServiceOrder.query.filter_by(company_id=company_id).order_by(ServiceOrder.date.desc()).limit(10).all(),
        }

service = ServiceActivity()
