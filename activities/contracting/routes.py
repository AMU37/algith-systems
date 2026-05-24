from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from core import db
from core.models import (
    Project, Claim, DailyAttendance, DailyPayment,
    MaterialPurchase, MaterialItem, Client, Supplier, Employee
)
from datetime import datetime, date

contracting_bp = Blueprint('contracting', __name__, url_prefix='/contracting', template_folder='templates')

# ==================== المشاريع ====================
@contracting_bp.route('/projects')
@login_required
def projects():
    projects_list = Project.query.filter_by(company_id=current_user.company_id).all()
    return render_template('contracting/projects.html', title='المشاريع', projects=projects_list)

@contracting_bp.route('/add_project', methods=['POST'])
@login_required
def add_project():
    try:
        project = Project(
            company_id=current_user.company_id,
            name=request.form.get('name'),
            client_id=request.form.get('client_id') or None,
            contract_number=request.form.get('contract_number'),
            contract_value=float(request.form.get('contract_value', 0)),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            status=request.form.get('status', 'active'),
            description=request.form.get('description'),
            location=request.form.get('location')
        )
        db.session.add(project)
        db.session.commit()
        flash('تم إضافة المشروع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.projects'))

@contracting_bp.route('/edit_project/<int:id>', methods=['POST'])
@login_required
def edit_project(id):
    project = Project.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        project.name = request.form.get('name')
        project.client_id = request.form.get('client_id') or None
        project.contract_number = request.form.get('contract_number')
        project.contract_value = float(request.form.get('contract_value', 0))
        project.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
        project.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None
        project.status = request.form.get('status', 'active')
        project.description = request.form.get('description')
        project.location = request.form.get('location')
        db.session.commit()
        flash('تم تحديث المشروع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.projects'))

@contracting_bp.route('/delete_project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(project)
        db.session.commit()
        flash('تم حذف المشروع بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.projects'))

# ==================== المواد ====================
@contracting_bp.route('/materials')
@login_required
def materials():
    # جلب المواد من المشتريات (مميزة)
    materials = db.session.query(MaterialItem.material_name, MaterialItem.unit,
                                  db.func.avg(MaterialItem.price).label('avg_price'),
                                  db.func.sum(MaterialItem.quantity).label('total_quantity'))\
        .join(MaterialPurchase)\
        .filter(MaterialPurchase.company_id == current_user.company_id)\
        .group_by(MaterialItem.material_name, MaterialItem.unit)\
        .all()
    return render_template('contracting/materials.html', title='المواد', materials=materials)

@contracting_bp.route('/add_material', methods=['POST'])
@login_required
def add_material():
    # هذا لإضافة مادة كمنتج في نظام المخزون
    # يمكنك إضافة نموذج Material منفصل إذا أردت
    flash('هذه الخاصية قيد التطوير', 'info')
    return redirect(url_for('contracting.materials'))

# ==================== المستخلصات ====================
@contracting_bp.route('/claims')
@login_required
def claims():
    claims_list = Claim.query.filter_by(company_id=current_user.company_id).all()
    projects = Project.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('contracting/claims.html', title='المستخلصات', claims=claims_list, projects=projects)

@contracting_bp.route('/add_claim', methods=['POST'])
@login_required
def add_claim():
    try:
        claim = Claim(
            company_id=current_user.company_id,
            project_id=request.form.get('project_id'),
            claim_number=request.form.get('claim_number'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
            amount=float(request.form.get('amount', 0)),
            approved_amount=float(request.form.get('approved_amount', 0)),
            paid_amount=float(request.form.get('paid_amount', 0)),
            completion_percentage=float(request.form.get('completion_percentage', 0)),
            status=request.form.get('status', 'pending'),
            notes=request.form.get('notes'),
            created_by=current_user.id
        )
        db.session.add(claim)
        db.session.commit()
        flash('تم إضافة المستخلص بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.claims'))

@contracting_bp.route('/edit_claim/<int:id>', methods=['POST'])
@login_required
def edit_claim(id):
    claim = Claim.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        claim.project_id = request.form.get('project_id')
        claim.claim_number = request.form.get('claim_number')
        claim.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today()
        claim.amount = float(request.form.get('amount', 0))
        claim.approved_amount = float(request.form.get('approved_amount', 0))
        claim.paid_amount = float(request.form.get('paid_amount', 0))
        claim.completion_percentage = float(request.form.get('completion_percentage', 0))
        claim.status = request.form.get('status', 'pending')
        claim.notes = request.form.get('notes')
        db.session.commit()
        flash('تم تحديث المستخلص بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.claims'))

@contracting_bp.route('/pay_claim/<int:id>', methods=['POST'])
@login_required
def pay_claim(id):
    claim = Claim.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        amount = float(request.form.get('amount', 0))
        claim.paid_amount = (claim.paid_amount or 0) + amount
        if claim.paid_amount >= claim.approved_amount:
            claim.status = 'paid'
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.claims'))

@contracting_bp.route('/delete_claim/<int:id>', methods=['POST'])
@login_required
def delete_claim(id):
    claim = Claim.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(claim)
        db.session.commit()
        flash('تم حذف المستخلص بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.claims'))

# ==================== مشتريات المواد ====================
@contracting_bp.route('/material_purchases')
@login_required
def material_purchases():
    purchases = MaterialPurchase.query.filter_by(company_id=current_user.company_id).order_by(MaterialPurchase.date.desc()).all()
    suppliers = Supplier.query.filter_by(company_id=current_user.company_id).all()
    projects = Project.query.filter_by(company_id=current_user.company_id).all()
    return render_template('contracting/material_purchases.html',
                         title='مشتريات المواد',
                         purchases=purchases,
                         suppliers=suppliers,
                         projects=projects,
                         now=date.today().strftime('%Y-%m-%d'))

@contracting_bp.route('/add_material_purchase', methods=['POST'])
@login_required
def add_material_purchase():
    try:
        purchase = MaterialPurchase(
            company_id=current_user.company_id,
            supplier_id=request.form.get('supplier_id') or None,
            project_id=request.form.get('project_id') or None,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
            total=float(request.form.get('total', 0)),
            paid=float(request.form.get('paid', 0)),
            payment_method=request.form.get('payment_method', 'cash'),
            notes=request.form.get('notes'),
            invoice_number=request.form.get('invoice_number'),
            created_by=current_user.id
        )
        db.session.add(purchase)
        db.session.flush()  # للحصول على ID

        # إضافة أصناف المشتريات
        item_index = 0
        while True:
            item_name = request.form.get(f'item_name_{item_index}')
            if not item_name:
                break
            item = MaterialItem(
                purchase_id=purchase.id,
                material_name=item_name,
                quantity=float(request.form.get(f'item_qty_{item_index}', 0)),
                unit=request.form.get(f'item_unit_{item_index}'),
                price=float(request.form.get(f'item_price_{item_index}', 0)),
                total=float(request.form.get(f'item_qty_{item_index}', 0)) * float(request.form.get(f'item_price_{item_index}', 0))
            )
            db.session.add(item)
            item_index += 1

        db.session.commit()
        flash('تم تسجيل عملية الشراء بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.material_purchases'))

@contracting_bp.route('/delete_material_purchase/<int:id>', methods=['POST'])
@login_required
def delete_material_purchase(id):
    purchase = MaterialPurchase.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(purchase)
        db.session.commit()
        flash('تم حذف عملية الشراء بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.material_purchases'))

# ==================== الحضور اليومي ====================
@contracting_bp.route('/daily_attendance')
@login_required
def daily_attendance():
    today_date = request.args.get('date', date.today().isoformat())
    attendances = DailyAttendance.query.filter_by(company_id=current_user.company_id, date=today_date).order_by(DailyAttendance.date.desc()).all()
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    projects = Project.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('contracting/daily_attendance.html',
                         title='الحضور اليومي',
                         attendances=attendances,
                         employees=employees,
                         projects=projects,
                         today=today_date)

@contracting_bp.route('/delete_attendance/<int:id>', methods=['POST'])
@login_required
def delete_attendance(id):
    att = DailyAttendance.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(att)
        db.session.commit()
        flash('تم حذف سجل الحضور', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.daily_attendance'))

@contracting_bp.route('/add_attendance', methods=['POST'])
@login_required
def add_attendance():
    try:
        attendance = DailyAttendance(
            company_id=current_user.company_id,
            employee_id=request.form.get('employee_id'),
            project_id=request.form.get('project_id') or None,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
            status=request.form.get('status', 'present'),
            hours=float(request.form.get('hours', 0)),
            daily_wage=float(request.form.get('daily_wage', 0)),
            notes=request.form.get('notes')
        )
        db.session.add(attendance)
        db.session.commit()
        flash('تم تسجيل الحضور بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.daily_attendance'))

# ==================== الدفعات اليومية ====================
@contracting_bp.route('/daily_payments')
@login_required
def daily_payments():
    payments = DailyPayment.query.filter_by(company_id=current_user.company_id).order_by(DailyPayment.date.desc()).all()
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    projects = Project.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('contracting/daily_payments.html',
                         title='الدفعات اليومية',
                         payments=payments,
                         employees=employees,
                         projects=projects)

@contracting_bp.route('/add_payment', methods=['POST'])
@login_required
def add_payment():
    try:
        payment = DailyPayment(
            company_id=current_user.company_id,
            employee_id=request.form.get('employee_id'),
            project_id=request.form.get('project_id') or None,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(),
            amount=float(request.form.get('amount', 0)),
            payment_method=request.form.get('payment_method', 'cash'),
            notes=request.form.get('notes')
        )
        db.session.add(payment)
        db.session.commit()
        flash('تم تسجيل الدفعة بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('contracting.daily_payments'))

# ==================== لوحة التحكم ====================
@contracting_bp.route('/dashboard')
@login_required
def dashboard():
    # إحصائيات للوحة التحكم
    stats = {
        'active_projects': Project.query.filter_by(company_id=current_user.company_id, status='active').count(),
        'total_claims': Claim.query.filter_by(company_id=current_user.company_id).count(),
        'total_purchases': MaterialPurchase.query.filter_by(company_id=current_user.company_id).count(),
        'total_attendance': DailyAttendance.query.filter_by(company_id=current_user.company_id).count(),
        'recent_projects': Project.query.filter_by(company_id=current_user.company_id).order_by(Project.created_at.desc()).limit(5).all(),
        'recent_claims': Claim.query.filter_by(company_id=current_user.company_id).order_by(Claim.date.desc()).limit(5).all()
    }
    return render_template('contracting/dashboard.html', title='لوحة تحكم المقاولات', stats=stats)