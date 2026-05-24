# activities/contracting/__init__.py
from ..base.activity_base import BaseActivity

class ContractingActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=1,
            name='شركة مقاولات',
            code='contracting',
            icon='fa-helmet-safety',
            description='إدارة المشاريع والمستخلصات والمواد'
        )

    def get_models(self):
        from .models import Project, Claim, DailyAttendance, DailyPayment, MaterialPurchase, MaterialItem
        return [Project, Claim, DailyAttendance, DailyPayment, MaterialPurchase, MaterialItem]

    def get_permissions(self):
        return [
            {'code': 'projects', 'name': 'المشاريع', 'default': False},
            {'code': 'claims', 'name': 'المستخلصات', 'default': False},
            {'code': 'attendance', 'name': 'الحضور اليومي', 'default': False},
            {'code': 'daily_payments', 'name': 'الدفعات اليومية', 'default': False},
            {'code': 'materials', 'name': 'المواد', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import Project, Claim, MaterialPurchase, DailyAttendance
        return {
            'projects_count': Project.query.filter_by(company_id=company_id).count(),
            'active_projects': Project.query.filter_by(company_id=company_id, status='active').count(),
            'pending_claims': Claim.query.filter_by(company_id=company_id, status='pending').count(),
            'total_claims': Claim.query.filter_by(company_id=company_id).count(),
            'total_purchases': db.session.query(db.func.sum(MaterialPurchase.total)).filter_by(company_id=company_id).scalar() or 0,
            'total_attendance': DailyAttendance.query.filter_by(company_id=company_id).count(),
            'recent_claims': Claim.query.filter_by(company_id=company_id).order_by(Claim.date.desc()).limit(5).all(),
            'recent_projects': Project.query.filter_by(company_id=company_id).order_by(Project.created_at.desc()).limit(5).all(),
        }

contracting = ContractingActivity()
