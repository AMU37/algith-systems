from ..base.activity_base import BaseActivity

class TransportActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=9,
            name='نقل',
            code='transport',
            icon='fa-truck',
            description='إدارة المركبات والرحلات والوقود'
        )

    def get_models(self):
        from .models import Vehicle, Trip, FuelRecord, VehicleMaintenance
        return [Vehicle, Trip, FuelRecord, VehicleMaintenance]

    def get_permissions(self):
        return [
            {'code': 'vehicles', 'name': 'المركبات', 'default': False},
            {'code': 'trips', 'name': 'الرحلات', 'default': False},
            {'code': 'fuel', 'name': 'الوقود', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import Vehicle, Trip
        from datetime import date
        return {
            'vehicles_count': Vehicle.query.filter_by(company_id=company_id, status='active').count(),
            'today_trips': Trip.query.filter_by(company_id=company_id, date=date.today()).count(),
            'total_revenue': db.session.query(db.func.sum(Trip.revenue)).filter_by(company_id=company_id).scalar() or 0,
            'pending_trips': Trip.query.filter_by(company_id=company_id, status='pending').count(),
            'recent_trips': Trip.query.filter_by(company_id=company_id).order_by(Trip.date.desc()).limit(10).all(),
        }

transport = TransportActivity()
