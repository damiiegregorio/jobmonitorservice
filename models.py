from datetime import datetime
from config import db, ma
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    job_id = db.Column(UUID(as_uuid=True), default=uuid4)
    app_name = db.Column(db.String(32), index=True)
    state = db.Column(db.String(32))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class JobSchema(ma.ModelSchema):
    class Meta:
        model = Job
        sqla_session = db.session