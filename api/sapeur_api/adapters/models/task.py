from datetime import datetime
from sqlalchemy import MetaData, String, TIMESTAMP, Table

from ...domain.models.task import Task
from ...extensions import db


metadata = MetaData()

tasks_lines = db.Table(
    'task', metadata,
    db.Column('id', String(100), primary_key=True),
    db.Column('title', String(100)),
    db.Column('description', String(255)),
    db.Column('creator_id', String(100)),
    db.Column('started_at', TIMESTAMP()),
    db.Column('done_at', TIMESTAMP()),
    db.Column('created_at', TIMESTAMP(), default=datetime.now()),
    db.Column('updated_at', TIMESTAMP(), default=datetime.now())
)

db.mapper(Task, tasks_lines)

