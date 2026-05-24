from ..base.activity_base import BaseActivity

class SchoolActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=7,
            name='مدرسة',
            code='school',
            icon='fa-school',
            description='إدارة الطلاب والمواد والامتحانات والرسوم'
        )

    def get_models(self):
        from .models import Student, Subject, Exam, Fee
        return [Student, Subject, Exam, Fee]

    def get_permissions(self):
        return [
            {'code': 'students', 'name': 'الطلاب', 'default': False},
            {'code': 'subjects', 'name': 'المواد', 'default': False},
            {'code': 'exams', 'name': 'الامتحانات', 'default': False},
            {'code': 'fees', 'name': 'الرسوم', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core import db
        from core.models import Student, Subject, Fee
        return {
            'students_count': Student.query.filter_by(company_id=company_id, status='active').count(),
            'subjects_count': Subject.query.filter_by(company_id=company_id, status='active').count(),
            'total_fees': db.session.query(db.func.sum(Fee.amount)).filter_by(company_id=company_id).scalar() or 0,
            'pending_fees': Fee.query.filter_by(company_id=company_id, status='pending').count(),
            'recent_exams': [],
        }

school = SchoolActivity()
