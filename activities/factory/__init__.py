from ..base.activity_base import BaseActivity

class FactoryActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=5,
            name='مصنع',
            code='factory',
            icon='fa-industry',
            description='إدارة الإنتاج والجودة والآلات'
        )

    def get_models(self):
        from .models import ProductionOrder, QualityCheck, Machine
        return [ProductionOrder, QualityCheck, Machine]

    def get_permissions(self):
        return [
            {'code': 'production', 'name': 'الإنتاج', 'default': False},
            {'code': 'quality', 'name': 'الجودة', 'default': False},
            {'code': 'machines', 'name': 'الآلات', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core.models import ProductionOrder, Machine, QualityCheck
        return {
            'production_orders': ProductionOrder.query.filter_by(company_id=company_id).count(),
            'machines_count': Machine.query.filter_by(company_id=company_id, status='active').count(),
            'quality_checks': QualityCheck.query.filter_by(company_id=company_id).count(),
            'recent_orders': ProductionOrder.query.filter_by(company_id=company_id).order_by(ProductionOrder.start_date.desc()).limit(10).all(),
        }

factory = FactoryActivity()
