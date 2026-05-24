from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Vehicle, Trip, FuelRecord, VehicleMaintenance, Employee, Client
from datetime import datetime, date

transport_bp = Blueprint('transport', __name__, url_prefix='/transport', template_folder='templates')

@transport_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('transport/dashboard.html', vehicles_count=Vehicle.query.filter_by(company_id=current_user.company_id, status='active').count(), today_trips=Trip.query.filter_by(company_id=current_user.company_id, date=date.today()).count(), total_revenue=db.session.query(db.func.sum(Trip.revenue)).filter_by(company_id=current_user.company_id).scalar() or 0, pending_trips=Trip.query.filter_by(company_id=current_user.company_id, status='pending').count(), recent_trips=Trip.query.filter_by(company_id=current_user.company_id).order_by(Trip.date.desc()).limit(10).all())

@transport_bp.route('/vehicles')
@login_required
def vehicles():
    vehicles_list = Vehicle.query.filter_by(company_id=current_user.company_id).all()
    return render_template('transport/vehicles.html', vehicles=vehicles_list)

@transport_bp.route('/add_vehicle', methods=['POST'])
@login_required
def add_vehicle():
    try:
        vehicle = Vehicle(company_id=current_user.company_id, plate_number=request.form.get('plate_number'), type=request.form.get('type'), model=request.form.get('model'), year=int(request.form.get('year', 0)) if request.form.get('year') else None, capacity=float(request.form.get('capacity', 0)), status=request.form.get('status', 'active'), notes=request.form.get('notes'))
        db.session.add(vehicle); db.session.commit()
        flash('تم إضافة المركبة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.vehicles'))

@transport_bp.route('/edit_vehicle/<int:id>', methods=['POST'])
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        vehicle.plate_number = request.form.get('plate_number'); vehicle.type = request.form.get('type')
        vehicle.model = request.form.get('model')
        vehicle.year = int(request.form.get('year', 0)) if request.form.get('year') else None
        vehicle.capacity = float(request.form.get('capacity', 0))
        vehicle.status = request.form.get('status', 'active'); vehicle.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث المركبة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.vehicles'))

@transport_bp.route('/delete_vehicle/<int:id>', methods=['POST'])
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(vehicle); db.session.commit()
        flash('تم حذف المركبة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.vehicles'))

@transport_bp.route('/trips')
@login_required
def trips():
    trips_list = Trip.query.filter_by(company_id=current_user.company_id).order_by(Trip.date.desc()).all()
    vehicles_list = Vehicle.query.filter_by(company_id=current_user.company_id).all()
    drivers = Employee.query.filter_by(company_id=current_user.company_id, status='active').all()
    clients_list = Client.query.filter_by(company_id=current_user.company_id).all()
    return render_template('transport/trips.html', trips=trips_list, vehicles=vehicles_list, drivers=drivers, clients=clients_list, now=date.today().strftime('%Y-%m-%d'))

@transport_bp.route('/add_trip', methods=['POST'])
@login_required
def add_trip():
    try:
        trip = Trip(company_id=current_user.company_id, vehicle_id=request.form.get('vehicle_id') or None, driver_id=request.form.get('driver_id') or None, client_id=request.form.get('client_id') or None, from_location=request.form.get('from_location'), to_location=request.form.get('to_location'), date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), cost=float(request.form.get('cost', 0)), revenue=float(request.form.get('revenue', 0)), status=request.form.get('status', 'pending'), notes=request.form.get('notes'))
        db.session.add(trip); db.session.commit()
        flash('تم إضافة الرحلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.trips'))

@transport_bp.route('/edit_trip/<int:id>', methods=['POST'])
@login_required
def edit_trip(id):
    trip = Trip.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        trip.vehicle_id = request.form.get('vehicle_id') or None; trip.driver_id = request.form.get('driver_id') or None
        trip.client_id = request.form.get('client_id') or None; trip.from_location = request.form.get('from_location')
        trip.to_location = request.form.get('to_location')
        trip.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today()
        trip.cost = float(request.form.get('cost', 0)); trip.revenue = float(request.form.get('revenue', 0))
        trip.status = request.form.get('status', 'pending'); trip.notes = request.form.get('notes')
        db.session.commit(); flash('تم تحديث الرحلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.trips'))

@transport_bp.route('/delete_trip/<int:id>', methods=['POST'])
@login_required
def delete_trip(id):
    trip = Trip.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(trip); db.session.commit()
        flash('تم حذف الرحلة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.trips'))

@transport_bp.route('/fuel')
@login_required
def fuel():
    fuel_records = FuelRecord.query.filter_by(company_id=current_user.company_id).order_by(FuelRecord.date.desc()).all()
    vehicles_list = Vehicle.query.filter_by(company_id=current_user.company_id).all()
    return render_template('transport/fuel.html', fuel=fuel_records, vehicles=vehicles_list, now=date.today().strftime('%Y-%m-%d'))

@transport_bp.route('/add_fuel', methods=['POST'])
@login_required
def add_fuel():
    try:
        record = FuelRecord(company_id=current_user.company_id, vehicle_id=request.form.get('vehicle_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), quantity=float(request.form.get('quantity', 0)), cost=float(request.form.get('cost', 0)), notes=request.form.get('notes'))
        db.session.add(record); db.session.commit()
        flash('تم تسجيل التموين بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.fuel'))

@transport_bp.route('/delete_fuel/<int:id>', methods=['POST'])
@login_required
def delete_fuel(id):
    record = FuelRecord.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(record); db.session.commit()
        flash('تم حذف سجل التموين بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.fuel'))

@transport_bp.route('/maintenance')
@login_required
def maintenance():
    maintenance_records = VehicleMaintenance.query.filter_by(company_id=current_user.company_id).order_by(VehicleMaintenance.date.desc()).all()
    vehicles_list = Vehicle.query.filter_by(company_id=current_user.company_id).all()
    return render_template('transport/vehicle_maintenance.html', maintenance=maintenance_records, vehicles=vehicles_list, now=date.today().strftime('%Y-%m-%d'))

@transport_bp.route('/add_vehicle_maintenance', methods=['POST'])
@login_required
def add_vehicle_maintenance():
    try:
        record = VehicleMaintenance(company_id=current_user.company_id, vehicle_id=request.form.get('vehicle_id') or None, date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else date.today(), type=request.form.get('type'), cost=float(request.form.get('cost', 0)), description=request.form.get('description'))
        db.session.add(record); db.session.commit()
        flash('تم تسجيل الصيانة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.maintenance'))

@transport_bp.route('/delete_vehicle_maintenance/<int:id>', methods=['POST'])
@login_required
def delete_vehicle_maintenance(id):
    record = VehicleMaintenance.query.filter_by(id=id, company_id=current_user.company_id).first_or_404()
    try:
        db.session.delete(record); db.session.commit()
        flash('تم حذف سجل الصيانة بنجاح', 'success')
    except Exception as e:
        db.session.rollback(); flash(f'حدث خطأ: {str(e)}', 'danger')
    return redirect(url_for('transport.maintenance'))
