from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Student, Subject, Exam, Fee, Employee
from datetime import datetime, date

school_bp = Blueprint('school', __name__, url_prefix='/school', template_folder='templates')

@school_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('school/dashboard.html', students_count=Student.query.filter_by(company_id=current_user.company_id, status='active').count(), subjects_count=Subject.query.filter_by(company_id=current_user.company_id, status='active').count(), total_fees=db.session.query(db.func.sum(Fee.amount)).filter_by(company_id=current_user.company_id).scalar() or 0, pending_fees=Fee.query.filter_by(company_id=current_user.company_id, status='pending').count(), recent_exams=Exam.query.filter_by(company_id=current_user.company_id).order_by(Exam.date.desc()).limit(10).all())

@school_bp.route('/students')
@login_required
def students():
    students_list = Student.query.filter_by(company_id=current_user.company_id).order_by(Student.id.desc()).all()
    return render_template('school/students.html', students=students_list)

@school_bp.route('/add_student', methods=['POST'])
@login_required
def add_student():
    try:
        student = Student(company_id=current_user.company_id, name=request.form.get('name'), student_id=request.form.get('student_id'), grade=request.form.get('grade'), class_name=request.form.get('class_name'), phone=request.form.get('phone'), parent_name=request.form.get('parent_name'), parent_phone=request.form.get('parent_phone'), status=request.form.get('status', 'active'))
        db.session.add(student); db.session.commit()
        flash('تم إضافة الطالب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.students'))

@school_bp.route('/edit_student/<int:id>', methods=['POST'])
@login_required
def edit_student(id):
    student = Student.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        student.name = request.form.get('name'); student.student_id = request.form.get('student_id')
        student.grade = request.form.get('grade'); student.class_name = request.form.get('class_name')
        student.phone = request.form.get('phone'); student.parent_name = request.form.get('parent_name')
        student.parent_phone = request.form.get('parent_phone'); student.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث بيانات الطالب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.students'))

@school_bp.route('/delete_student/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    student = Student.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(student); db.session.commit()
        flash('تم حذف الطالب بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.students'))

@school_bp.route('/subjects')
@login_required
def subjects():
    subjects_list = Subject.query.filter_by(company_id=current_user.company_id).all()
    teachers = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    return render_template('school/subjects.html', subjects=subjects_list, teachers=teachers)

@school_bp.route('/add_subject', methods=['POST'])
@login_required
def add_subject():
    try:
        subject = Subject(company_id=current_user.company_id, name=request.form.get('name'), grade=request.form.get('grade'), teacher_id=request.form.get('teacher_id') or None, status=request.form.get('status', 'active'))
        db.session.add(subject); db.session.commit()
        flash('تم إضافة المادة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.subjects'))

@school_bp.route('/edit_subject/<int:id>', methods=['POST'])
@login_required
def edit_subject(id):
    subject = Subject.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        subject.name = request.form.get('name'); subject.grade = request.form.get('grade')
        subject.teacher_id = request.form.get('teacher_id') or None
        subject.status = request.form.get('status', 'active')
        db.session.commit(); flash('تم تحديث المادة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.subjects'))

@school_bp.route('/delete_subject/<int:id>', methods=['POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(subject); db.session.commit()
        flash('تم حذف المادة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.subjects'))

@school_bp.route('/exams')
@login_required
def exams():
    exams_list = Exam.query.filter_by(company_id=current_user.company_id).order_by(Exam.date.desc()).all()
    subjects_list = Subject.query.filter_by(company_id=current_user.company_id).all()
    students_list = Student.query.filter_by(company_id=current_user.company_id).all()
    return render_template('school/exams.html', exams=exams_list, subjects=subjects_list, students=students_list, now=date.today().strftime('%Y-%m-%d'))

@school_bp.route('/add_exam', methods=['POST'])
@login_required
def add_exam():
    try:
        exam = Exam(company_id=current_user.company_id, subject_id=request.form.get('subject_id') or None, student_id=request.form.get('student_id') or None, score=float(request.form.get('score', 0)), max_score=float(request.form.get('max_score', 100)), date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), exam_type=request.form.get('exam_type'))
        db.session.add(exam); db.session.commit()
        flash('تم إضافة الامتحان بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.exams'))

@school_bp.route('/delete_exam/<int:id>', methods=['POST'])
@login_required
def delete_exam(id):
    exam = Exam.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(exam); db.session.commit()
        flash('تم حذف الامتحان بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.exams'))

@school_bp.route('/fees')
@login_required
def fees():
    fees_list = Fee.query.filter_by(company_id=current_user.company_id).all()
    students_list = Student.query.filter_by(company_id=current_user.company_id).all()
    return render_template('school/fees.html', fees=fees_list, students=students_list)

@school_bp.route('/add_fee', methods=['POST'])
@login_required
def add_fee():
    try:
        fee = Fee(company_id=current_user.company_id, student_id=request.form.get('student_id') or None, amount=float(request.form.get('amount', 0)), paid=float(request.form.get('paid', 0)), due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date() if request.form.get('due_date') else None, status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
        db.session.add(fee); db.session.commit()
        flash('تم إضافة الرسوم بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.fees'))

@school_bp.route('/pay_fee/<int:id>', methods=['POST'])
@login_required
def pay_fee(id):
    fee = Fee.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        extra = float(request.form.get('amount', 0))
        fee.paid = (fee.paid or 0) + extra
        if fee.paid >= fee.amount: fee.status = 'paid'
        else: fee.status = 'partial'
        db.session.commit(); flash('تم تسجيل الدفع بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.fees'))

@school_bp.route('/delete_fee/<int:id>', methods=['POST'])
@login_required
def delete_fee(id):
    fee = Fee.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(fee); db.session.commit()
        flash('تم حذف الرسوم بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('school.fees'))
