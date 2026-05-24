# activities/restaurant/__init__.py
from ..base.activity_base import BaseActivity

class RestaurantActivity(BaseActivity):
    """نشاط المطاعم"""
    
    def __init__(self):
        super().__init__(
            activity_id=3,
            name='مطعم / كافتيريا',
            code='restaurant',
            icon='fa-utensils',
            description='إدارة المطاعم - قوائم الطعام، الطلبات، الفواتير'
        )
    
    def get_models(self):
        from .models import MenuItem, TableOrder, OrderItem
        return [MenuItem, TableOrder, OrderItem]
    
    def get_permissions(self):
        return [
            {'code': 'menu', 'name': 'قائمة الطعام', 'default': False},
            {'code': 'orders', 'name': 'الطلبات', 'default': False},
        ]
    
    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import MenuItem, TableOrder
        from datetime import date
        return {
            'menu_count': MenuItem.query.filter_by(company_id=company_id, status='active').count(),
            'today_orders': TableOrder.query.filter_by(company_id=company_id, date=date.today()).count(),
            'today_revenue': db.session.query(db.func.sum(TableOrder.total)).filter_by(company_id=company_id, date=date.today()).scalar() or 0,
            'pending_orders': TableOrder.query.filter_by(company_id=company_id, status='pending').count(),
            'recent_orders': TableOrder.query.filter_by(company_id=company_id).order_by(TableOrder.date.desc()).limit(10).all(),
        }

# إنشاء النشاط
restaurant = RestaurantActivity()