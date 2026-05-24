# activities/retail/__init__.py
from ..base.activity_base import BaseActivity

class RetailActivity(BaseActivity):
    """نشاط متاجر التجزئة"""
    
    def __init__(self):
        super().__init__(
            activity_id=2,
            name='متجر / بقالة',
            code='retail',
            icon='fa-store',
            description='إدارة المنتجات والمبيعات والمخزون'
        )
    
    def get_models(self):
        from .models import Product, Purchase, PurchaseItem, SalesInvoice, SalesInvoiceItem
        return [Product, Purchase, PurchaseItem, SalesInvoice, SalesInvoiceItem]
    
    def get_permissions(self):
        return [
            {'code': 'products', 'name': 'المنتجات', 'default': False},
            {'code': 'purchases', 'name': 'المشتريات', 'default': False},
            {'code': 'sales', 'name': 'المبيعات', 'default': False},
            {'code': 'inventory', 'name': 'المخزون', 'default': False},
        ]
    
    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import Product, SalesInvoice
        from datetime import date
        return {
            'products_count': Product.query.filter_by(company_id=company_id, status='active').count(),
            'today_sales': SalesInvoice.query.filter_by(company_id=company_id, date=date.today()).count(),
            'today_revenue': db.session.query(db.func.sum(SalesInvoice.total)).filter_by(company_id=company_id, date=date.today()).scalar() or 0,
            'low_stock': Product.query.filter(Product.company_id == company_id, Product.quantity <= Product.min_quantity).count(),
        }

# إنشاء النشاط
retail = RetailActivity()