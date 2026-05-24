from core import db
from datetime import datetime, date, time


class ShiftType(db.Model):
    __tablename__ = 'et_shift_type'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    work_days = db.Column(db.Integer, default=6)
    vacation_days = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Bus(db.Model):
    __tablename__ = 'et_bus'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    plate_number = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, default=30)
    model = db.Column(db.String(100))
    color = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Driver(db.Model):
    __tablename__ = 'et_driver'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    license_number = db.Column(db.String(50))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(80), nullable=True)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='et_driver', foreign_keys=[user_id])


class TransportRoute(db.Model):
    __tablename__ = 'et_route'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(200))
    departure_time = db.Column(db.Time, nullable=False)
    return_time = db.Column(db.Time, nullable=False)
    work_days = db.Column(db.String(200), default='[]')
    shift_type_id = db.Column(db.Integer, db.ForeignKey('et_shift_type.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('et_bus.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('et_driver.id'))
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shift_type = db.relationship('ShiftType', backref='routes')
    bus = db.relationship('Bus', backref='routes')
    driver = db.relationship('Driver', backref='routes')


class EmployeeAssignment(db.Model):
    __tablename__ = 'et_assignment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('et_route.id'), nullable=False)
    shift_type_id = db.Column(db.Integer, db.ForeignKey('et_shift_type.id'))
    is_residential = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref='transport_assignments')
    route = db.relationship('TransportRoute', backref='assignments')
    shift_type = db.relationship('ShiftType', backref='assignments')


class TripRoute(db.Model):
    """ربط الرحلات بخطوط سير متعددة (دمج مناطق)"""
    __tablename__ = 'et_trip_route'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('et_trip.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('et_route.id'), nullable=False)
    order = db.Column(db.Integer, default=0)

    route = db.relationship('TransportRoute', backref='trip_links')


class ETTrip(db.Model):
    __tablename__ = 'et_trip'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('et_route.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('et_bus.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('et_driver.id'))
    date = db.Column(db.Date, nullable=False, default=date.today)
    departure_time = db.Column(db.Time)
    return_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='scheduled')
    departure_note = db.Column(db.Text)
    return_note = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    route = db.relationship('TransportRoute', backref='et_trips', foreign_keys=[route_id])
    bus = db.relationship('Bus', backref='et_trips')
    driver = db.relationship('Driver', backref='et_trips')
    trip_routes = db.relationship('TripRoute', backref='trip', cascade='all, delete-orphan',
                                   order_by='TripRoute.order')


class RideLog(db.Model):
    __tablename__ = 'et_ride_log'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('et_trip.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='on_time')
    method = db.Column(db.String(20), default='manual')
    notes = db.Column(db.Text)

    trip = db.relationship('ETTrip', backref='ride_logs')
    employee = db.relationship('Employee', backref='transport_ride_logs')


class Violation(db.Model):
    __tablename__ = 'et_violation'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('et_trip.id'), nullable=True)
    violation_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, default=date.today)
    resolved = db.Column(db.Boolean, default=False)
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolved_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    employee = db.relationship('Employee', backref='transport_violations')
    trip = db.relationship('ETTrip', backref='violations')


class EmployeeTransportInfo(db.Model):
    __tablename__ = 'et_employee_info'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    department = db.Column(db.String(100))
    shift_type_id = db.Column(db.Integer, db.ForeignKey('et_shift_type.id'), nullable=True)
    shift_start_date = db.Column(db.Date)
    work_day = db.Column(db.String(20))
    movement_status = db.Column(db.String(50))
    is_administrative = db.Column(db.Boolean, default=True)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    route_id = db.Column(db.Integer, db.ForeignKey('et_route.id'), nullable=True)
    external_company = db.Column(db.String(200))
    city = db.Column(db.String(100))
    residence_location = db.Column(db.String(200))
    transport_type = db.Column(db.String(50), default='يومي')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('et_info', uselist=False))
    shift_type = db.relationship('ShiftType', backref='employee_infos')
    route = db.relationship('TransportRoute', backref='employee_infos')
