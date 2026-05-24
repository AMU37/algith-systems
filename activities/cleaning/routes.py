from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import WorkSite, SupervisorReport, Visit, Complaint, Team, TeamMember, Client, Employee
from datetime import datetime, date

cleaning_bp = Blueprint('cleaning', __name__, url_prefix='/cleaning', template_folder='templates')

@cleaning_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('cleaning/dashboard.html', clients_count=Client.query.filter_by(company_id=current_user.company_id, status='active').count(), teams_count=Team.query.filter_by(company_id=current_user.company_id, status='active').count(), active_contracts=0, today_visits=Visit.query.filter_by(company_id=current_user.company_id, date=date.today()).count(), recent_visits=Visit.query.filter_by(company_id=current_user.company_id).order_by(Visit.date.desc()).limit(10).all())

@cleaning_bp.route('/work-sites')
@login_required
def work_sites():
    sites = WorkSite.query.filter_by(company_id=current_user.company_id).order_by(WorkSite.id.desc()).all()
    clients = Client.query.filter_by(company_id=current_user.company_id, status='active').all()
    supervisors = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('cleaning/work_sites.html', sites=sites, clients=clients, supervisors=supervisors)

@cleaning_bp.route('/add_work_site', methods=['POST'])
@login_required
def add_work_site():
    try:
        site = WorkSite(company_id=current_user.company_id, name=request.form.get('name'), client_id=request.form.get('client_id') or None, address=request.form.get('address'), supervisor_id=request.form.get('supervisor_id') or None, worker_count=int(request.form.get('worker_count', 0)), work_hours=request.form.get('work_hours'), status=request.form.get('status', 'active'), notes=request.form.get('notes'))
        db.session.add(site); db.session.commit()
        flash('تم إضافة الموقع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.work_sites'))

@cleaning_bp.route('/edit_work_site/<int:id>', methods=['POST'])
@login_required
def edit_work_site(id):
    site = WorkSite.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        site.name = request.form.get('name'); site.client_id = request.form.get('client_id') or None
        site.address = request.form.get('address'); site.supervisor_id = request.form.get('supervisor_id') or None
        site.worker_count = int(request.form.get('worker_count', 0)); site.work_hours = request.form.get('work_hours')
        site.status = request.form.get('status', 'active'); site.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث الموقع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.work_sites'))

@cleaning_bp.route('/delete_work_site/<int:id>', methods=['POST'])
@login_required
def delete_work_site(id):
    site = WorkSite.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(site); db.session.commit()
        flash('تم حذف الموقع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.work_sites'))

@cleaning_bp.route('/teams')
@login_required
def teams():
    teams_list = Team.query.filter_by(company_id=current_user.company_id).all()
    supervisors = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    sites = WorkSite.query.filter_by(company_id=current_user.company_id, status='active').all()
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('cleaning/teams.html', teams=teams_list, supervisors=supervisors, sites=sites, employees=employees)

@cleaning_bp.route('/add_team', methods=['POST'])
@login_required
def add_team():
    try:
        team = Team(company_id=current_user.company_id, name=request.form.get('name'), supervisor_id=request.form.get('supervisor_id') or None, site_id=request.form.get('site_id') or None, status=request.form.get('status', 'active'))
        db.session.add(team); db.session.flush()
        member_ids = request.form.getlist('member_ids')
        for emp_id in member_ids:
            if emp_id:
                db.session.add(TeamMember(team_id=team.id, employee_id=int(emp_id)))
        db.session.commit(); flash('تم إضافة الفريق بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.teams'))

@cleaning_bp.route('/delete_team/<int:id>', methods=['POST'])
@login_required
def delete_team(id):
    team = Team.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(team); db.session.commit()
        flash('تم حذف الفريق بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.teams'))

@cleaning_bp.route('/visits')
@login_required
def visits():
    visits_list = Visit.query.filter_by(company_id=current_user.company_id).order_by(Visit.date.desc()).all()
    sites = WorkSite.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('cleaning/visits.html', visits=visits_list, sites=sites, now=date.today().strftime('%Y-%m-%d'))

@cleaning_bp.route('/add_visit', methods=['POST'])
@login_required
def add_visit():
    try:
        visit = Visit(company_id=current_user.company_id, site_id=request.form.get('site_id') or None, visitor_id=current_user.id, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), notes=request.form.get('notes'), rating=int(request.form.get('rating', 0)) if request.form.get('rating') else None)
        db.session.add(visit); db.session.commit()
        flash('تم تسجيل الزيارة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.visits'))

@cleaning_bp.route('/supervisor-reports')
@login_required
def supervisor_reports():
    reports = SupervisorReport.query.filter_by(company_id=current_user.company_id).order_by(SupervisorReport.date.desc()).all()
    sites = WorkSite.query.filter_by(company_id=current_user.company_id, status='active').all()
    supervisors = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('cleaning/supervisor_reports.html', reports=reports, sites=sites, supervisors=supervisors, now=date.today().strftime('%Y-%m-%d'))

@cleaning_bp.route('/add_supervisor_report', methods=['POST'])
@login_required
def add_supervisor_report():
    try:
        report = SupervisorReport(company_id=current_user.company_id, site_id=request.form.get('site_id') or None, supervisor_id=request.form.get('supervisor_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), report=request.form.get('report'), issues=request.form.get('issues'), status=request.form.get('status', 'submitted'))
        db.session.add(report); db.session.commit()
        flash('تم إضافة التقرير بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.supervisor_reports'))

@cleaning_bp.route('/complaints')
@login_required
def complaints():
    complaints_list = Complaint.query.filter_by(company_id=current_user.company_id).order_by(Complaint.date.desc()).all()
    clients = Client.query.filter_by(company_id=current_user.company_id).all()
    sites = WorkSite.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('cleaning/complaints.html', complaints=complaints_list, clients=clients, sites=sites, now=date.today().strftime('%Y-%m-%d'))

@cleaning_bp.route('/add_complaint', methods=['POST'])
@login_required
def add_complaint():
    try:
        complaint = Complaint(company_id=current_user.company_id, client_id=request.form.get('client_id') or None, site_id=request.form.get('site_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), description=request.form.get('description'), status=request.form.get('status', 'pending'))
        db.session.add(complaint); db.session.commit()
        flash('تم تسجيل الشكوى بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.complaints'))

@cleaning_bp.route('/resolve_complaint/<int:id>', methods=['POST'])
@login_required
def resolve_complaint(id):
    complaint = Complaint.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        complaint.status = request.form.get('status', 'resolved')
        complaint.resolution = request.form.get('resolution')
        from datetime import datetime as dt
        complaint.resolved_at = dt.utcnow()
        db.session.commit(); flash('تم حل الشكوى بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('cleaning.complaints'))
