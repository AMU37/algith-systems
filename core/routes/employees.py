# core/routes/employees.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from core import db
from core.models import Employee, Area, DailyAttendance, Project, DailyPayment, Salary, Evaluation, EvaluationCriteria, Deduction, Addition, Advance, User
from datetime import datetime, date, timedelta
import json

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')


# ==================== عرض الموظفين ====================
@employees_bp.route('/')
@login_required
def employees():
    company_id = current_user.company_id
    emps = Employee.query.filter_by(company_id=company_id).order_by(Employee.id.desc()).all()
    areas = Area.query.filter_by(company_id=company_id, status='active').all() if 'Area' in globals() else []
    bt = current_user.company.business_type if current_user.company else 'general'
    ctx = {'employees': emps, 'areas': areas, 'title': 'الموظفين', 'business_type': bt}
    if bt == 'employee_transport':
        from activities.employee_transport.models import ETShiftType, ETRoute, EmployeeTransportInfo
        ctx['et_shift_types'] = ETShiftType.query.filter_by(company_id=company_id, status='active').all()
        ctx['et_routes'] = ETRoute.query.filter_by(company_id=company_id, status='active').all()
        ctx['et_infos'] = {e.employee_id: e for e in EmployeeTransportInfo.query.filter_by(company_id=company_id).all()}
    return render_template('employees.html', **ctx)


# ==================== إضافة موظف ====================
@employees_bp.route('/add', methods=['POST'])
@login_required
def add_employee():
    try:
        company_id = current_user.company_id

        # حساب الرواتب حسب نوع الأجر
        wage_type = request.form.get('wage_type', 'monthly')
        daily_wage = float(request.form.get('daily_wage') or 0)
        comprehensive_salary = float(request.form.get('comprehensive_salary') or 0)
        basic_salary = float(request.form.get('basic_salary') or 0)

        if wage_type == 'daily' and daily_wage > 0:
            comprehensive_salary = daily_wage * 30
            basic_salary = daily_wage * 26

        # إنشاء الموظف
        code = request.form.get('code', '').strip()
        if not code:
            bt = current_user.company.business_type if current_user.company else 'general'
            if bt == 'employee_transport':
                last = Employee.query.filter(Employee.company_id == company_id, Employee.code.like('ET-%')).order_by(Employee.id.desc()).first()
                n = int(last.code.split('-')[1]) if last and last.code and '-' in last.code else 0
                code = f'ET-{n+1:03d}'
            else:
                last = Employee.query.filter_by(company_id=company_id).order_by(Employee.id.desc()).first()
                code = f'EMP-{company_id:03d}-{(last.id or 0)+1:03d}'
        emp = Employee(
            company_id=company_id,
            name=request.form.get('name'),
            card_number=request.form.get('card_number'),
            code=code,
            birth_date=datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get(
                'birth_date') else None,
            birth_place=request.form.get('birth_place'),
            position=request.form.get('position'),
            join_date=datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date() if request.form.get(
                'join_date') else date.today(),
            wage_type=wage_type,
            comprehensive_salary=comprehensive_salary,
            basic_salary=basic_salary,
            daily_wage=daily_wage,
            area=request.form.get('area'),
            notes=request.form.get('notes')
        )
        db.session.add(emp)
        db.session.flush()

        # حفظ بيانات نقل الموظفين
        bt = current_user.company.business_type if current_user.company else 'general'
        if bt == 'employee_transport':
            from activities.employee_transport.models import EmployeeTransportInfo
            dep = request.form.get('et_department', '').strip()
            st_id = request.form.get('et_shift_type_id')
            r_id = request.form.get('et_route_id')
            at = request.form.get('et_arrival_time')
            dt = request.form.get('et_departure_time')
            if dep or st_id or r_id:
                et_info = EmployeeTransportInfo(
                    employee_id=emp.id, company_id=company_id,
                    department=dep or None,
                    shift_type_id=int(st_id) if st_id else None,
                    shift_start_date=datetime.strptime(request.form.get('et_shift_start_date'), '%Y-%m-%d').date() if request.form.get('et_shift_start_date') else None,
                    work_day=request.form.get('et_work_day'),
                    movement_status=request.form.get('et_movement_status'),
                    arrival_time=datetime.strptime(at, '%H:%M').time() if at else None,
                    departure_time=datetime.strptime(dt, '%H:%M').time() if dt else None,
                    route_id=int(r_id) if r_id else None,
                    city=request.form.get('et_city'),
                    residence_location=request.form.get('et_residence_location'),
                    transport_type=request.form.get('et_transport_type', 'ورديات')
                )
                db.session.add(et_info)

        # إنشاء حساب مستخدم للموظف إذا تم الاختيار
        if request.form.get('create_user') == 'on':
            username = request.form.get('user_username') or emp.code or f"emp_{emp.id}"
            password = request.form.get('user_password') or '123456'

            if not User.query.filter_by(company_id=company_id, username=username).first():
                new_user = User(
                    company_id=company_id,
                    username=username,
                    full_name=emp.name,
                    role='user',
                    is_active=True
                )
                new_user.set_password(password)
                db.session.add(new_user)

        db.session.commit()
        flash('تم إضافة الموظف بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.employees'))


# ==================== تعديل موظف ====================
@employees_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit_employee(id):
    try:
        emp = Employee.query.get(id)
        if not emp or emp.company_id != current_user.company_id:
            flash('الموظف غير موجود', 'error')
            return redirect(url_for('employees.employees'))

        # تحديث البيانات
        emp.name = request.form.get('name', emp.name)
        emp.card_number = request.form.get('card_number', emp.card_number)
        emp.code = request.form.get('code', emp.code)
        emp.birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date() if request.form.get(
            'birth_date') else emp.birth_date
        emp.birth_place = request.form.get('birth_place', emp.birth_place)
        emp.position = request.form.get('position', emp.position)
        emp.join_date = datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date() if request.form.get(
            'join_date') else emp.join_date
        emp.wage_type = request.form.get('wage_type', emp.wage_type)
        emp.daily_wage = float(request.form.get('daily_wage') or emp.daily_wage)
        emp.comprehensive_salary = float(request.form.get('comprehensive_salary') or emp.comprehensive_salary)
        emp.basic_salary = float(request.form.get('basic_salary') or emp.basic_salary)
        emp.area = request.form.get('area', emp.area)
        emp.status = request.form.get('status', emp.status)
        emp.notes = request.form.get('notes', emp.notes)

        # إعادة حساب الرواتب إذا كان الأجر يومي
        if emp.wage_type == 'daily' and emp.daily_wage > 0:
            emp.comprehensive_salary = emp.daily_wage * 30
            emp.basic_salary = emp.daily_wage * 26

        # تحديث بيانات نقل الموظفين
        bt = current_user.company.business_type if current_user.company else 'general'
        if bt == 'employee_transport':
            from activities.employee_transport.models import EmployeeTransportInfo
            et_info = EmployeeTransportInfo.query.filter_by(employee_id=emp.id).first()
            dep = request.form.get('et_department', '').strip()
            st_id = request.form.get('et_shift_type_id')
            r_id = request.form.get('et_route_id')
            at = request.form.get('et_arrival_time')
            lv = request.form.get('et_departure_time')
            if et_info:
                et_info.department = dep or None
                et_info.shift_type_id = int(st_id) if st_id else None
                et_info.shift_start_date = datetime.strptime(request.form.get('et_shift_start_date'), '%Y-%m-%d').date() if request.form.get('et_shift_start_date') else None
                et_info.work_day = request.form.get('et_work_day')
                et_info.movement_status = request.form.get('et_movement_status')
                et_info.arrival_time = datetime.strptime(at, '%H:%M').time() if at else None
                et_info.departure_time = datetime.strptime(lv, '%H:%M').time() if lv else None
                et_info.route_id = int(r_id) if r_id else None
                et_info.city = request.form.get('et_city')
                et_info.residence_location = request.form.get('et_residence_location')
                et_info.transport_type = request.form.get('et_transport_type', 'يومي')
            elif dep or st_id or r_id:
                et_info = EmployeeTransportInfo(
                    employee_id=emp.id, company_id=emp.company_id,
                    department=dep or None,
                    shift_type_id=int(st_id) if st_id else None,
                    shift_start_date=datetime.strptime(request.form.get('et_shift_start_date'), '%Y-%m-%d').date() if request.form.get('et_shift_start_date') else None,
                    work_day=request.form.get('et_work_day'),
                    movement_status=request.form.get('et_movement_status'),
                    arrival_time=datetime.strptime(at, '%H:%M').time() if at else None,
                    departure_time=datetime.strptime(lv, '%H:%M').time() if lv else None,
                    route_id=int(r_id) if r_id else None,
                    city=request.form.get('et_city'),
                    residence_location=request.form.get('et_residence_location'),
                    transport_type=request.form.get('et_transport_type', 'ورديات')
                )
                db.session.add(et_info)

        db.session.commit()
        flash('تم تعديل بيانات الموظف بنجاح', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.employees'))


# ==================== حذف موظف ====================
@employees_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    try:
        emp = Employee.query.get(id)
        if emp and emp.company_id == current_user.company_id:
            emp.status = 'deleted'
            db.session.commit()
            flash('تم حذف الموظف بنجاح', 'success')
        else:
            flash('الموظف غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.employees'))


# ==================== الحضور ====================
@employees_bp.route('/attendance')
@login_required
def attendance():
    today_date = request.args.get('date', date.today().isoformat())
    attendances = DailyAttendance.query.filter_by(
        company_id=current_user.company_id,
        date=today_date
    ).all() if 'DailyAttendance' in globals() else []

    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    projects = Project.query.filter_by(company_id=current_user.company_id,
                                       status='active').all() if 'Project' in globals() else []

    return render_template('attendance.html',
                           attendances=attendances,
                           employees=employees,
                           projects=projects,
                           today=today_date,
                           title='الحضور')


@employees_bp.route('/attendance/add', methods=['POST'])
@login_required
def add_attendance():
    try:
        if 'DailyAttendance' not in globals():
            flash('وحدة الحضور غير مفعلة', 'error')
            return redirect(url_for('employees.attendance'))

        att = DailyAttendance(
            company_id=current_user.company_id,
            employee_id=int(request.form.get('employee_id')),
            project_id=int(request.form.get('project_id')) if request.form.get('project_id') else None,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            status=request.form.get('status', 'present'),
            hours=float(request.form.get('hours') or 0),
            daily_wage=float(request.form.get('daily_wage') or 0),
            notes=request.form.get('notes')
        )
        db.session.add(att)
        db.session.commit()
        flash('تم تسجيل الحضور بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.attendance'))


@employees_bp.route('/attendance/bulk', methods=['POST'])
@login_required
def bulk_attendance():
    try:
        att_date = request.form.get('date', date.today().isoformat())
        employee_ids = request.form.getlist('employee_ids')
        proj_id = request.form.get('project_id')

        for emp_id in employee_ids:
            if emp_id:
                emp = Employee.query.get(int(emp_id))
                if emp:
                    dw = emp.daily_wage if emp.wage_type == 'daily' else (
                        emp.basic_salary / 30 if emp.basic_salary else 0)
                    att = DailyAttendance(
                        company_id=current_user.company_id,
                        employee_id=emp.id,
                        project_id=int(proj_id) if proj_id else None,
                        date=datetime.strptime(att_date, '%Y-%m-%d').date(),
                        status='present',
                        daily_wage=dw
                    )
                    db.session.add(att)

        db.session.commit()
        flash('تم تسجيل الحضور الجماعي بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.attendance', date=att_date))


@employees_bp.route('/attendance/delete/<int:id>', methods=['POST'])
@login_required
def delete_attendance(id):
    try:
        att = DailyAttendance.query.get(id)
        if att and att.company_id == current_user.company_id:
            db.session.delete(att)
            db.session.commit()
            flash('تم حذف سجل الحضور', 'success')
        else:
            flash('السجل غير موجود', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')
    return redirect(url_for('employees.attendance'))

# ==================== الدفعات اليومية ====================
@employees_bp.route('/daily-payments')
@login_required
def daily_payments():
    payments = DailyPayment.query.filter_by(company_id=current_user.company_id).order_by(
        DailyPayment.date.desc()).all() if 'DailyPayment' in globals() else []
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    projects = Project.query.filter_by(company_id=current_user.company_id,
                                       status='active').all() if 'Project' in globals() else []

    return render_template('daily_payments.html',
                           payments=payments,
                           employees=employees,
                           projects=projects,
                           title='الدفعات اليومية')


@employees_bp.route('/daily-payment/add', methods=['POST'])
@login_required
def add_daily_payment():
    try:
        if 'DailyPayment' not in globals():
            flash('وحدة الدفعات اليومية غير مفعلة', 'error')
            return redirect(url_for('employees.daily_payments'))

        dp = DailyPayment(
            company_id=current_user.company_id,
            employee_id=int(request.form.get('employee_id')),
            project_id=int(request.form.get('project_id')) if request.form.get('project_id') else None,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            amount=float(request.form.get('amount') or 0),
            payment_method=request.form.get('payment_method', 'cash'),
            notes=request.form.get('notes')
        )
        db.session.add(dp)
        db.session.commit()
        flash('تم صرف الدفعة اليومية بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.daily_payments'))


@employees_bp.route('/daily-payment/delete/<int:id>', methods=['POST'])
@login_required
def delete_daily_payment(id):
    try:
        dp = DailyPayment.query.get(id)
        if dp and dp.company_id == current_user.company_id:
            db.session.delete(dp)
            db.session.commit()
            flash('تم حذف الدفعة', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.daily_payments'))


# ==================== الرواتب ====================
@employees_bp.route('/salaries')
@login_required
def salaries():
    month = request.args.get('month', date.today().strftime('%Y-%m'))
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()

    salary_data = []
    for emp in employees:
        salary = Salary.query.filter_by(company_id=current_user.company_id, employee_id=emp.id,
                                        month=month).first() if 'Salary' in globals() else None

        if salary:
            salary_data.append({'employee': emp, 'salary': salary})
        else:
            # حساب مؤقت للراتب
            base = emp.comprehensive_salary if emp.wage_type == 'monthly' else (emp.daily_wage * 30)
            salary_data.append({'employee': emp, 'salary': None, 'net': base,
                                'total_additions': 0, 'total_deductions': 0, 'advances_deduction': 0})

    return render_template('salaries.html', salary_data=salary_data, month=month, title='الرواتب')


@employees_bp.route('/salary/generate/<month>', methods=['POST'])
@login_required
def generate_salaries(month):
    try:
        employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()

        for emp in employees:
            # تجنب التكرار
            if Salary.query.filter_by(company_id=current_user.company_id, employee_id=emp.id, month=month).first():
                continue

            base = emp.comprehensive_salary if emp.wage_type == 'monthly' else (emp.daily_wage * 30)

            salary = Salary(
                company_id=current_user.company_id,
                employee_id=emp.id,
                month=month,
                basic_salary=emp.basic_salary,
                net_salary=base
            )
            db.session.add(salary)

        db.session.commit()
        flash('تم إنشاء الرواتب بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.salaries', month=month))


@employees_bp.route('/salary/pay/<int:id>', methods=['POST'])
@login_required
def pay_salary(id):
    try:
        salary = Salary.query.get(id)
        if salary and salary.company_id == current_user.company_id:
            salary.is_paid = True
            salary.paid_date = date.today()
            db.session.commit()
            flash(f'تم صرف راتب {salary.month} بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.salaries', month=salary.month if salary else None))


# ==================== التقييمات ====================
@employees_bp.route('/evaluations')
@login_required
def evaluations():
    evaluations_list = Evaluation.query.filter_by(company_id=current_user.company_id).order_by(
        Evaluation.date.desc()).all() if 'Evaluation' in globals() else []
    employees = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    criteria = EvaluationCriteria.query.filter_by(company_id=current_user.company_id,
                                                  status='active').all() if 'EvaluationCriteria' in globals() else []

    return render_template('evaluations.html',
                           evaluations=evaluations_list,
                           employees=employees,
                           criteria=criteria,
                           title='التقييمات')


@employees_bp.route('/evaluation/add', methods=['POST'])
@login_required
def add_evaluation():
    try:
        if 'Evaluation' not in globals():
            flash('وحدة التقييم غير مفعلة', 'error')
            return redirect(url_for('employees.evaluations'))

        ev = Evaluation(
            company_id=current_user.company_id,
            employee_id=int(request.form.get('employee_id')),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            total_score=float(request.form.get('total_score') or 0),
            notes=request.form.get('notes'),
            evaluator_id=current_user.id
        )
        db.session.add(ev)
        db.session.commit()
        flash('تم إضافة التقييم بنجاح', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'خطأ: {str(e)}', 'error')

    return redirect(url_for('employees.evaluations'))


# ==================== API للموظف (لجلب بيانات موظف) ====================
@employees_bp.route('/api/<int:id>')
@login_required
def api_employee(id):
    emp = Employee.query.get(id)
    if not emp or emp.company_id != current_user.company_id:
        return jsonify({})

    return jsonify({
        'id': emp.id,
        'name': emp.name,
        'card_number': emp.card_number or '',
        'code': emp.code or '',
        'position': emp.position or '',
        'birth_date': str(emp.birth_date) if emp.birth_date else '',
        'birth_place': emp.birth_place or '',
        'join_date': str(emp.join_date) if emp.join_date else '',
        'area': emp.area or 'غير محدد',
        'basic_salary': emp.basic_salary,
        'comprehensive_salary': emp.comprehensive_salary,
        'daily_wage': emp.daily_wage,
        'wage_type': emp.wage_type or 'monthly',
        'status': emp.status,
        'notes': emp.notes or '',
        'et_department': emp.et_info.department if emp.et_info else '',
        'et_shift_type_id': emp.et_info.shift_type_id if emp.et_info else '',
        'et_shift_start_date': str(emp.et_info.shift_start_date) if emp.et_info and emp.et_info.shift_start_date else '',
        'et_work_day': emp.et_info.work_day if emp.et_info else '',
        'et_movement_status': emp.et_info.movement_status if emp.et_info else '',
        'et_arrival_time': str(emp.et_info.arrival_time)[:5] if emp.et_info and emp.et_info.arrival_time else '',
        'et_departure_time': str(emp.et_info.departure_time)[:5] if emp.et_info and emp.et_info.departure_time else '',
        'et_route_id': emp.et_info.route_id if emp.et_info else '',
        'et_city': emp.et_info.city if emp.et_info else '',
        'et_residence_location': emp.et_info.residence_location if emp.et_info else '',
        'et_transport_type': emp.et_info.transport_type if emp.et_info else 'يومي'
    })