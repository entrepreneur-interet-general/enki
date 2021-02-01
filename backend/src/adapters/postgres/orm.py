import logging

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, String, ForeignKey, Integer, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import ChoiceType

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entity import EvenementType, EvenementEntity
from domain.messages.entities.message_entity import MessageType, Severity, MessageEntity
from domain.messages.entities.resource import ResourceEntity
from domain.messages.entities.tag_entity import TagEntity
from domain.users.entities.group import GroupType, GroupEntity
from domain.users.entities.user import UserEntity
from domain.users.entities.contact import ContactEntity

logger = logging.getLogger(__name__)

metadata = MetaData()

tagMessageTable = Table(
    'tags_messages', metadata,
    Column('messages_uuid', String(60), ForeignKey("messages.uuid")),
    Column('tag_uuid', String(60), ForeignKey("tags.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

usersCompanyTable = Table(
    'users_group', metadata,
    Column('user_uuid', String(60), ForeignKey("users.uuid")),
    Column('group_uuid', String(60), ForeignKey("groups.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

contactsCompanyTable = Table(
    'contacts_companies', metadata,
    Column('contact_uuid', String(60), ForeignKey("contacts.uuid")),
    Column('group_uuid', String(60), ForeignKey("groups.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

users_favorites_contact_table = Table(
    'users_favorites_contact', metadata,
    Column('user_uuid', String(60), ForeignKey("users.uuid")),
    Column('contact_uuid', String(60), ForeignKey("contacts.uuid")),
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
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)

usersTable = Table(
    'users', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False),
    Column('position', String(255), nullable=False),
    Column('evenement_id', String(60), ForeignKey("evenements.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


groupTable = Table(
    'groups', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('name', String(255), nullable=False),
    Column('type', Enum(GroupType), nullable=False),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


contactTable = Table(
    'contacts', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('address', String(255), nullable=False),
    Column('tel', JSONB()),
    Column('position', String(255), nullable=False),
    Column('group_name', String(255), nullable=False),
    Column('updated_at', TIMESTAMP(), nullable=True, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=True, default=datetime.now)
)


def start_mappers():
    mapper(TagEntity, tagTable)
    mapper(EvenementEntity, evenementsTable)
    mapper(ResourceEntity, resourceTable)
    mapper(SimpleAffairEntity, affairsTable)
    mapper(GroupEntity, groupTable)
    mapper(UserEntity, usersTable,
           properties={
               'groups': relationship(GroupEntity, backref='users', secondary=usersCompanyTable),
               'contacts': relationship(ContactEntity, backref='users', secondary=users_favorites_contact_table),
           }
   )

    mapper(ContactEntity, contactTable,
           properties={
            'groups': relationship(GroupEntity, backref='contacts', secondary=contactsCompanyTable),
        })
    mapper(
        MessageEntity, messagesTable,
        properties={
            'tags': relationship(TagEntity, backref='messages', secondary=tagMessageTable),
            'resources': relationship(ResourceEntity, backref='messages')
        }
    )
