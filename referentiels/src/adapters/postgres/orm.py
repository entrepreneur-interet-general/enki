import logging

from sqlalchemy import Table, MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import mapper

from ...domain.elus.maires.entity import MaireEntity

logger = logging.getLogger(__name__)
metadata = MetaData()


def start_mappers(engine: Engine):

    metadata = MetaData(engine)
    maires_table = Table('maires', metadata, autoload=True)
    mapper(MaireEntity, maires_table)
