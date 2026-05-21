import sys
import os
project_home = '/home/Alimubark93/alghith'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.chdir(project_home)
instance_dir = os.path.join(project_home, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

from app import app as application, init_db, db, Company, User
import json
from datetime import date, timedelta

# Run init to create SUPER company if missing
with application.app_context():
    db.create_all()
    
    # Create SUPER company
    super_company = Company.query.filter_by(code='SUPER').first()
    if not super_company:
        super_company = Company(
            name='Al-Ghaith SaaS', code='SUPER', business_type='general',
            is_active=True, subscription_status='active', is_blocked=False
        )
        db.session.add(super_company)
        db.session.flush()
        print('Created SUPER company, id:', super_company.id)
    
    # Fix super_admin user
    sa = User.query.filter_by(username='superadmin').first()
    if sa:
        sa.company_id = super_company.id
        sa.is_active = True
        sa.role = 'super_admin'
        db.session.commit()
        print('Fixed super_admin user')
    else:
        sa = User(
            company_id=super_company.id, username='superadmin',
            full_name='Super Admin', role='super_admin', is_active=True,
            permissions=json.dumps({p: True for p in ['employees','salaries','suppliers','clients','products','purchases','sales','accounting','reports','areas','admin']})
        )
        sa.set_password('superadmin123')
        db.session.add(sa)
        db.session.commit()
        print('Created super_admin user')
