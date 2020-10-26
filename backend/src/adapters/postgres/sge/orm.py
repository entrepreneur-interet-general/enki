import logging

from sqlalchemy import (
    Table, MetaData, Column, String, Text, TIMESTAMP, ARRAY
)
from sqlalchemy.engine import Engine

from sqlalchemy.orm import mapper
from domain.affairs.entities.sge.sge_message_entity import SgeMessageEntity

logger = logging.getLogger(__name__)

metadata = MetaData()


def start_mappers(engine: Engine):
    message_recu_table = Table(
        'message_recu', metadata,
        Column('id', String(255), primary_key=True),
        Column('emetteur', String(255)),
        Column('type', String(255)),
        Column('destinataires', ARRAY(String(255))),
        Column('date_emission', TIMESTAMP()),
        Column('message_brut', Text()),
        autoload=True,
        autoload_with=engine
    )
    mapper(SgeMessageEntity, message_recu_table)
