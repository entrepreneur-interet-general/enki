import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from typing import Dict, Any

from adapters.postgres.orm import start_mappers, metadata
from domain.messages.ports.message_repository import AbstractMessageRepository


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
def information_in_memory_repo() -> AbstractInformationRepository:
    information_repo = InMemoryInformationRepository()
    information_repo._informations = []
    return information_repo


@pytest.fixture(scope="session")
def information_pg_repo(sqlite_engine: Engine) -> AbstractInformationRepository:
    clear_mappers()
    start_mappers()
    information_repository = PgInformationRepository(sessionmaker(bind=sqlite_engine, autoflush=False)())
    return information_repository


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # ,
def information_repo(request, information_in_memory_repo, information_pg_repo) -> AbstractInformationRepository:
    if request.param == "sqlite":
        repo = information_pg_repo
    else:  # request.param == "in_memory"
        repo = information_in_memory_repo
        repo._informations = []
    return repo