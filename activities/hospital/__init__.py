from ..base.activity_base import BaseActivity

class HospitalActivity(BaseActivity):
    def __init__(self):
        super().__init__(
            activity_id=6,
            name='مستشفى',
            code='hospital',
            icon='fa-hospital',
            description='إدارة المرضى والأطباء والمواعيد'
        )

    def get_models(self):
        from .models import Patient, Doctor, Appointment, LabTest, Medicine
        return [Patient, Doctor, Appointment, LabTest, Medicine]

    def get_permissions(self):
        return [
            {'code': 'patients', 'name': 'المرضى', 'default': False},
            {'code': 'doctors', 'name': 'الأطباء', 'default': False},
            {'code': 'appointments', 'name': 'المواعيد', 'default': False},
        ]

    def get_dashboard_stats(self, company_id):
        from core.models import Patient, Doctor, Appointment
        from datetime import date
        return {
            'patients_count': Patient.query.filter_by(company_id=company_id).count(),
            'doctors_count': Doctor.query.filter_by(company_id=company_id, status='active').count(),
            'today_appointments': Appointment.query.filter_by(company_id=company_id, date=date.today()).count(),
            'pending_appointments': Appointment.query.filter_by(company_id=company_id, status='scheduled').count(),
            'recent_appointments': Appointment.query.filter_by(company_id=company_id).order_by(Appointment.date.desc()).limit(10).all(),
        }

hospital = HospitalActivity()
