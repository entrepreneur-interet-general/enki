import os
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from adapters.postgres import PgTagRepository
from adapters.postgres.pg_affair_repository import PgAffairRepository
from adapters.postgres.pg_evenement_repository import PgEvenementRepository
from adapters.postgres.pg_message_repository import PgMessageRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.evenements.repository import AbstractEvenementRepository
from domain.messages.ports import AbstractMessageRepository
from domain.messages.ports.tag_repository import AbstractTagRepository


def build_engine(sql_engine_uri: str) -> Engine:

    isolation_level = "READ UNCOMMITTED" if "sqlite" in sql_engine_uri else "REPEATABLE READ"
    engine = create_engine(
        sql_engine_uri,
        isolation_level=isolation_level,
    )
    return engine


def get_pg_repos(engine: Engine) -> Tuple[AbstractTagRepository, AbstractMessageRepository, AbstractAffairRepository, AbstractEvenementRepository]:
    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()

    tag_repository = PgTagRepository(session)
    message_repository = PgMessageRepository(session)
    affair_repository = PgAffairRepository(session)
    evenement_repository = PgEvenementRepository(session)
    return tag_repository,message_repository, affair_repository, evenement_repository
