import logging
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, String, ForeignKey, Integer, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import ChoiceType

from adapters.postgres.orm.metadata import metadata
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entities.evenement_entity import EvenementType, EvenementEntity, EvenementRoleType, \
    UserEvenementRole
from domain.evenements.entities.message_entity import MessageType, Severity, MessageEntity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.users.entities.user import UserEntity

logger = logging.getLogger(__name__)

tagMessageTable = Table(
    'tags_messages', metadata,
    Column('messages_uuid', String(60), ForeignKey("messages.uuid")),
    Column('tag_uuid', String(60), ForeignKey("tags.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

messagesTable = Table(
    'messages', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(MessageType)),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('executor_id', String(60), ForeignKey("users.uuid"), nullable=True),
    Column('creator_id', String(60), ForeignKey("users.uuid")),
    Column('done_at', TIMESTAMP()),
    Column('started_at', TIMESTAMP()),
    Column('severity', ChoiceType(Severity, impl=Integer()), nullable=False),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
)

tagTable = Table(
    'tags', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False, unique=True),
    Column('creator_id', String(255), ForeignKey("users.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

user_evenement_role_table = Table(
    'user_evenement_roles', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('user_id', String(255), ForeignKey("users.uuid")),
    Column('evenement_id', String(255), ForeignKey("evenements.uuid")),
    Column('type', ChoiceType(EvenementRoleType, impl=String())),
    Column('revoked_at', TIMESTAMP(), nullable=True),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

resourceTable = Table(
    'resources', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('bucket_name', String(255), nullable=False, unique=False),
    Column('object_path', String(255), nullable=False, unique=False),
    Column('content_type', String(60), nullable=False, unique=False),
    Column('creator_id', String(255), ForeignKey("users.uuid")),
    Column('original_name', String(255)),  # ForeignKey("users.uuid")),
    Column('message_id', String(255), ForeignKey("messages.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

evenementsTable = Table(
    'evenements', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(255)),
    Column('type', Enum(EvenementType)),
    Column('creator_id', String(255), ForeignKey("users.uuid")),
    Column('started_at', TIMESTAMP(), nullable=False, default=datetime.now),
    Column('ended_at', TIMESTAMP(), nullable=True, default=None),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

affairsTable = Table(
    'affairs', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('sge_hub_id', String(255), nullable=False),
    Column("location", Geometry('POINT')),
    Column('affair', JSONB()),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


def start_mappers():
    mapper(TagEntity, tagTable)
    mapper(EvenementEntity, evenementsTable,
           properties={
               'creator': relationship(UserEntity, backref='evenements', foreign_keys=evenementsTable.c.creator_id,
                                       lazy='noload'),
               'user_roles': relationship(UserEvenementRole, backref='evenements', lazy='dynamic')
           }
           )
    mapper(ResourceEntity, resourceTable)
    mapper(UserEvenementRole, user_evenement_role_table,
           properties={
               'user': relationship(UserEntity, backref='user_evenement_roles'),
           }
           )
    mapper(SimpleAffairEntity, affairsTable,
           properties={
               'evenement': relationship(EvenementEntity, backref='affairs'),
           }
           )
    mapper(
        MessageEntity, messagesTable,
        properties={
            'tags': relationship(TagEntity, backref='messages', secondary=tagMessageTable),
            'resources': relationship(ResourceEntity, backref='messages'),
            'creator': relationship(UserEntity, backref='messages', foreign_keys=messagesTable.c.creator_id)
        }
    )
