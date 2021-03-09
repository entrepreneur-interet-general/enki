import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from adapters.postgres import PgTagRepository, PgMessageRepository
from adapters.postgres.orm import start_mappers, metadata
from domain.affairs.ports.affair_repository import InMemoryAffairRepository, AbstractAffairRepository
from domain.evenements.ports.message_repository import InMemoryMessageRepository, AbstractMessageRepository
from domain.evenements.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository


@pytest.fixture(scope="session")
def sqlite_engine() -> Engine:
    engine = create_engine('sqlite:///foo.db')
    return engine


@pytest.fixture(scope="session")
def session(sqlite_engine: Engine):
    return sessionmaker(bind=sqlite_engine, autoflush=False)()


@pytest.fixture(scope="function", autouse=True)
def clear_tables(sqlite_engine):
    metadata.drop_all(sqlite_engine)
    metadata.create_all(sqlite_engine)
    # [table.drop(sqlite_engine) for table in all_tables]


@pytest.fixture(scope="function")
def tag_in_memory_repo() -> AbstractTagRepository:
    tag_repo = InMemoryTagRepository()
    tag_repo._tags = []
    return tag_repo


@pytest.fixture(scope="function")
def message_in_memory_repo() -> AbstractMessageRepository:
    message_repo = InMemoryMessageRepository()
    message_repo._messages = []
    return message_repo



@pytest.fixture(scope="session")
def tag_pg_repo(session, sqlite_engine: Engine) -> AbstractTagRepository:
    clear_mappers()
    start_mappers()
    tag_repository = PgTagRepository(session)
    return tag_repository


@pytest.fixture(scope="session")
def message_pg_repo(session, sqlite_engine: Engine) -> AbstractMessageRepository:
    clear_mappers()
    start_mappers()
    message_repository = PgMessageRepository(session)
    return message_repository


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # ,
def tag_repo(request, tag_in_memory_repo, tag_pg_repo) -> AbstractTagRepository:
    if request.param == "sqlite":
        repo = tag_pg_repo
    else:  # request.param == "in_memory"
        repo = tag_in_memory_repo
        repo._tags = []
    return repo


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # , "sqlite"
def message_repo(request, message_in_memory_repo, message_pg_repo) -> AbstractMessageRepository:
    if request.param == "sqlite":
        repo = message_pg_repo
    else:  # request.param == "in_memory"
        repo = message_in_memory_repo
        repo._messages = []
    return repo


@pytest.fixture(scope="function")
def affair_in_memory_repo() -> AbstractAffairRepository:
    affair_repo = InMemoryAffairRepository()
    affair_repo._affairs = []
    return affair_repo


@pytest.fixture(scope="function", params=["in_memory"])  # , "sqlite"
def affair_repo(request, affair_in_memory_repo) -> AbstractAffairRepository:
    if request.param == "in_memory":
        repo = affair_in_memory_repo
        repo._affairs = []
        return repo
