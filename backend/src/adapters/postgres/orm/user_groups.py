from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from datetime import datetime
import sqlalchemy as sa

from sqlalchemy import Table, MetaData, Column, String, ForeignKey, Unicode, TIMESTAMP, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapper, relationship
from sqlalchemy_utils import TSVectorType
from geoalchemy2 import Geometry

from domain.users.entities.group import GroupType, GroupEntity, \
    LocationEntity, LocationType, UserPositionEntity,\
    PositionGroupTypeEntity

from domain.users.entities.user import UserEntity
from domain.users.entities.contact import ContactEntity
from adapters.postgres.orm.metadata import metadata

group_location_table = Table(
    'group_location', metadata,
    Column('group_uuid', String(60), ForeignKey("groups.uuid")),
    Column('location_uuid', String(60), ForeignKey("locations.uuid")),
)

users_group_table = Table(
    'users_group', metadata,
    Column('user_uuid', String(60), ForeignKey("users.uuid")),
    Column('group_uuid', String(60), ForeignKey("groups.uuid")),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now),
)

contacts_groups_table = Table(
    'contacts_groups', metadata,
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

usersTable = Table(
    'users', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False),
    Column('position_id', String(60), ForeignKey("users_positions.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=False, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=False, default=datetime.now)
)


groupTable = Table(
    'groups', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('label', String(255), nullable=False),
    Column('slug', String(255), nullable=False),
    Column('type', Enum(GroupType), nullable=False),
    Column('location_id', ForeignKey("locations.uuid")),
    Column('search_vector', TSVectorType('label'), nullable=True),
)

locationTable = Table(
    'locations', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('label', String(255), nullable=False),
    Column('search_label', String(255), nullable=False),
    Column('slug', String(255), nullable=False),
    Column('type', Enum(LocationType), nullable=False),
    Column('external_id', String(60), nullable=False, unique=True, index=True),
    Column('polygon', Geometry('POLYGON')),
    #Column('search_vector', TSVectorType('search_label'), nullable=True),
)

contactTable = Table(
    'contacts', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('address', String(255), nullable=False),
    Column('tel', JSONB()),
    Column('position_id', String(60), ForeignKey("users_positions.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=True, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=True, default=datetime.now)
)

position_group_type_table = Table(
    'positions_groups', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('label', String(255), nullable=False),
    Column('slug', String(255), nullable=False),
    Column('group_type', Enum(GroupType), nullable=False),
)

user_position_table = Table(
    'users_positions', metadata,
    Column('uuid', String(60), primary_key=True),
    Column('position_id', String(60), ForeignKey("positions_groups.uuid")),
    Column('group_id', String(60), ForeignKey("groups.uuid")),
    Column('updated_at', TIMESTAMP(), nullable=True, default=datetime.now, onupdate=datetime.now),
    Column('created_at', TIMESTAMP(), nullable=True, default=datetime.now)
)


def start_mappers():
    mapper(LocationEntity, locationTable)
    mapper(PositionGroupTypeEntity, position_group_type_table)
    mapper(UserPositionEntity, user_position_table,
           properties={
               'group': relationship(GroupEntity,  foreign_keys=user_position_table.c.group_id),
               'position': relationship(PositionGroupTypeEntity,  foreign_keys=user_position_table.c.position_id)
           }
   )

    mapper(GroupEntity, groupTable,
           properties={
               'location': relationship(LocationEntity, backref='groups')
           }
          )
    mapper(UserEntity, usersTable,
           properties={
               'position': relationship(UserPositionEntity, backref='users'),
               'contacts': relationship(ContactEntity, backref='users', secondary=users_favorites_contact_table,
                                        lazy='noload'),
           }
           )

    mapper(ContactEntity, contactTable,
           properties={
               'position': relationship(UserPositionEntity, backref='contacts'),
           })
