from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from ...adapters.postgres.orm import start_mappers
from ...adapters.postgres.pg_maire_repository import PgMaireRepository
from ...domain.elus.maires.repository import AbstractMaireRepository


def build_engine(sql_engine_uri: str) -> Engine:

    isolation_level = "READ UNCOMMITTED" if "sqlite" in sql_engine_uri else "REPEATABLE READ"
    engine = create_engine(
        sql_engine_uri,
        isolation_level=isolation_level,
    )
    return engine


def get_pg_repos(engine: Engine) -> AbstractMaireRepository:
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()

    maire_repository = PgMaireRepository(session)
    return maire_repository
