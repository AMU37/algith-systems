import sys
import os
project_home = '/home/Alimubark93/alghith'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
os.chdir(project_home)

from app import app, db, init_db

with app.app_context():
    db.create_all()
    print("DB Tables Created/Verified")

init_db()
