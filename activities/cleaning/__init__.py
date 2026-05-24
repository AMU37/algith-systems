from ..base.activity_base import BaseActivity

class CleaningActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=4,
            name='شركة نظافة',
            code='cleaning',
            icon='fa-hand-sparkles',
            description='إدارة عقود النظافة والفرق والزيارات'
        )

    def get_models(self):
        from .models import WorkSite, Visit, Complaint, Team, TeamMember
        return [WorkSite, Visit, Complaint, Team, TeamMember]

    def get_permissions(self):
        return [
            {'code': 'worksites', 'name': 'مواقع العمل', 'default': False},
            {'code': 'visits', 'name': 'الزيارات', 'default': False},
            {'code': 'teams', 'name': 'الفرق', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core.models import Client, Team, Visit, WorkSite
        from core import db
        from datetime import date
        return {
            'clients_count': Client.query.filter_by(company_id=company_id, status='active').count(),
            'teams_count': Team.query.filter_by(company_id=company_id, status='active').count(),
            'active_contracts': WorkSite.query.filter_by(company_id=company_id, status='active').count(),
            'today_visits': Visit.query.filter_by(company_id=company_id, date=date.today()).count(),
            'recent_visits': Visit.query.filter_by(company_id=company_id).order_by(Visit.date.desc()).limit(10).all(),
        }

cleaning = CleaningActivity()
