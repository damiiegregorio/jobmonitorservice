import os
from config import db
from models import Job
import uuid

# Data to initialize database with
JOBS = [
    # {'job_id ': uuid.uuid1(), 'app_name': 'Telegram', 'state': 'PROCESSING'},
    {'app_name': 'Telegram', 'state': 'PROCESSING'},
]

# Delete database file if it exists currently
if os.path.exists('people.db'):
    os.remove('people.db')


# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for job in JOBS:
    p = Job(app_name=job.get('app_name'), state=job.get('state'))
    db.session.add(p)

db.session.commit()
