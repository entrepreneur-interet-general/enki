import os
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from adapters.postgres import PgTagRepository
from adapters.postgres.orm import start_mappers
from adapters.postgres.pg_affair_repository import PgAffairRepository
from adapters.postgres.pg_task_repository import PgTaskRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository


def build_engine(sql_engine_uri: str) -> Engine:

    isolation_level = "READ UNCOMMITTED" if "sqlite" in sql_engine_uri else "REPEATABLE READ"
    engine = create_engine(
        sql_engine_uri,
        isolation_level=isolation_level,
    )
    return engine


def get_pg_repos(engine: Engine) -> Tuple[AbstractTagRepository, AbstractTaskRepository, AbstractAffairRepository]:
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()

    tag_repository = PgTagRepository(session)
    task_repository = PgTaskRepository(session, tag_repo=tag_repository)
    affair_repository = PgAffairRepository(session)
    return tag_repository, task_repository, affair_repository
