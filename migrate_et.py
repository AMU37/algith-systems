from core import create_app, db

app = create_app()
with app.app_context():
    import sqlalchemy as sa
    insp = sa.inspect(db.engine)
    # columns migration for et_driver
    cols = [c['name'] for c in insp.get_columns('et_driver')]
    if 'user_id' not in cols:
        db.session.execute(db.text('ALTER TABLE et_driver ADD COLUMN user_id INTEGER REFERENCES user(id)'))
        print('+ user_id')
    if 'username' not in cols:
        db.session.execute(db.text('ALTER TABLE et_driver ADD COLUMN username VARCHAR(80)'))
        print('+ username')
    # create et_employee_info table if not exists
    tables = insp.get_table_names()
    if 'et_employee_info' not in tables:
        db.session.execute(db.text('''
            CREATE TABLE et_employee_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL UNIQUE REFERENCES employee(id),
                company_id INTEGER NOT NULL REFERENCES company(id),
                department VARCHAR(100),
                shift_type_id INTEGER REFERENCES et_shift_type(id),
                shift_start_date DATE,
                work_day VARCHAR(20),
                movement_status VARCHAR(50),
                is_administrative BOOLEAN DEFAULT 1,
                arrival_time TIME,
                departure_time TIME,
                route_id INTEGER REFERENCES et_route(id),
                city VARCHAR(100),
                residence_location VARCHAR(200),
                transport_type VARCHAR(50) DEFAULT 'يومي',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''))
        print('+ et_employee_info table')
    # add work_days / vacation_days to et_shift_type
    cols_st = [c['name'] for c in insp.get_columns('et_shift_type')]
    if 'work_days' not in cols_st:
        db.session.execute(db.text('ALTER TABLE et_shift_type ADD COLUMN work_days INTEGER DEFAULT 6'))
        print('+ work_days')
    if 'vacation_days' not in cols_st:
        db.session.execute(db.text('ALTER TABLE et_shift_type ADD COLUMN vacation_days INTEGER DEFAULT 1'))
        print('+ vacation_days')
    # add external_company to et_employee_info
    cols_ei = [c['name'] for c in insp.get_columns('et_employee_info')]
    if 'external_company' not in cols_ei:
        db.session.execute(db.text('ALTER TABLE et_employee_info ADD COLUMN external_company VARCHAR(200)'))
        print('+ external_company')
    db.session.commit()
    print('done')
