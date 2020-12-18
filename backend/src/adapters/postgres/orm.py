import logging

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, String, ForeignKey, Integer, TIMESTAMP, Enum
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import mapper, relationship, clear_mappers
from sqlalchemy_utils import ChoiceType

from domain.evenements.entity import EvenementType, EvenementEntity
from domain.tasks.entities.event_entity import Severity
from domain.tasks.entities.task_entity import TaskEntity, TaskType
from domain.tasks.entities.tag_entity import TagEntity

logger = logging.getLogger(__name__)

metadata = MetaData()

userTable = Table(
    'users', metadata,
    Column('uuid', String(60), primary_key=True),
)

tagTaskTable = Table(
    'tag_task', metadata,
    Column('task_uuid', String(60), ForeignKey("tasks.uuid")),
    Column('tag_uuid', String(60), ForeignKey("tags.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

taskHierarchyTaskTable = Table(
    'task_hierarchy', metadata,
    Column('parent_task_uuid', String(60), ForeignKey("tasks.uuid")),
    Column('children_task_uuid', String(60), ForeignKey("tasks.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),

)

taskTable = Table(
    'tasks', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('task_type', Enum(TaskType)),
    Column('event_type', String(60)),
    Column('executor_id', String(60), ForeignKey("users.uuid")),
    Column('executor_type', String(60)),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('creator_type', String(60)),
    Column('done_at', TIMESTAMP()),
    Column('started_at', TIMESTAMP()),
    Column('severity', ChoiceType(Severity, impl=Integer()), nullable=False),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
)
tagTable = Table(
    'tags', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('creator_id', String(255)),  # ForeignKey("users.uuid")),
    Column('color', String(8)),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

evenementsTable = Table(
    'evenements', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(EvenementType)),
    Column('creator_id', String(255)),  # ForeignKey("users.uuid")),
    Column('started_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('ended_at', TIMESTAMP(), nullable=True, default=None),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

all_tables = [
    userTable,
    tagTaskTable,
    taskHierarchyTaskTable,
    taskTable,
    tagTable,
    evenementsTable
]


def start_mappers():
    mapper(TagEntity, tagTable)
    mapper(EvenementEntity, evenementsTable)
    mapper(
        TaskEntity, taskTable,
        properties={
            'tags': relationship(TagEntity, backref='tasks', secondary=tagTaskTable)
        }
    )
