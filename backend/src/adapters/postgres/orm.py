import logging

from sqlalchemy import (
    Table, MetaData, Column, String
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import mapper
from domain.tasks.entities.task_entity import TaskEntity

logger = logging.getLogger(__name__)

metadata = MetaData()

taskTable = Table(
    'tasks', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
)

def start_mappers(engine: Engine):
    metadata.create_all(engine)
    mapper(TaskEntity, taskTable)
