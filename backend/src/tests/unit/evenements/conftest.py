import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from adapters.postgres.orm import start_mappers, metadata
from adapters.postgres.pg_evenement_repository import PgEvenementRepository
from domain.evenements.repository import AbstractEvenementRepository, InMemoryEvenementRepository


@pytest.fixture(scope="session")
def sqlite_engine() -> Engine:
    engine = create_engine('sqlite:///foo.db')
    return engine


@pytest.fixture(scope="function", autouse=True)
def clear_tables(sqlite_engine):
    metadata.drop_all(sqlite_engine)
    metadata.create_all(sqlite_engine)
    # [table.drop(sqlite_engine) for table in all_tables]


@pytest.fixture(scope="function")
def evenement_in_memory_repo() -> AbstractEvenementRepository:
    evenement_repo = InMemoryEvenementRepository()
    evenement_repo._evenements = []
    return evenement_repo


@pytest.fixture(scope="session")
def evenement_pg_repo(sqlite_engine: Engine) -> AbstractEvenementRepository:
    clear_mappers()
    start_mappers(sqlite_engine)
    evenement_repository = PgEvenementRepository(sessionmaker(bind=sqlite_engine, autoflush=False)())
    return evenement_repository


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # ,
def evenement_repo(request, evenement_in_memory_repo, evenement_pg_repo) -> AbstractEvenementRepository:
    if request.param == "sqlite":
        repo = evenement_pg_repo
    else:  # request.param == "in_memory"
        repo = evenement_in_memory_repo
        repo._evenements = []
    return repo
