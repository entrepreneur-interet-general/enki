import os
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from adapters.postgres import PgTagRepository
from adapters.postgres.orm import start_mappers
from adapters.postgres.pg_task_repository import PgTaskRepository
from adapters.postgres.sge.orm import start_mappers as sge_mappers
from adapters.postgres.sge.pg_affairs_repository import PgSgeMessageRepository
from domain.affairs.ports.message_repository import AbstractSgeMessageRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository


def build_engine(sql_engine_uri: str) -> Engine:
    engine = create_engine(
        sql_engine_uri,
        isolation_level="REPEATABLE READ",
    )
    return engine


def get_pg_repos(engine: Engine) -> Tuple[AbstractTagRepository, AbstractTaskRepository]:
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()

    tag_repository = PgTagRepository(session)

    return tag_repository, PgTaskRepository(session, tag_repo=tag_repository)


def get_pg_message_repos() -> AbstractSgeMessageRepository:
    sge_engine = create_engine(
        os.environ.get('SQLALCHEMY_SGE_ENGINE_OPTIONS'),
        isolation_level="REPEATABLE READ", echo=True
    )

    sge_mappers(engine=sge_engine)
    session_factory = sessionmaker(bind=sge_engine)
    session: Session = session_factory()
    return PgSgeMessageRepository(session)
