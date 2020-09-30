from datetime import datetime
from sqlalchemy import MetaData, String, TIMESTAMP, Table
from ...domain.models.user import User
from ...extensions import db

metadata = MetaData()

users_lines = db.Table(
    'user', metadata,
    db.Column('id', String(100), primary_key=True),
    db.Column('username', String(100)),
    db.Column('email', String(255)),
    db.Column('password', String(100)),
    db.Column('created_at', TIMESTAMP(), default=datetime.now()),
    db.Column('updated_at', TIMESTAMP(), default=datetime.now())
)

db.mapper(User, users_lines)