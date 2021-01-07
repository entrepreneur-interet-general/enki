import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, clear_mappers

from adapters.postgres import PgTagRepository, PgTaskRepository
from adapters.postgres.orm import start_mappers, metadata
from domain.affairs.ports.affair_repository import InMemoryAffairRepository, AbstractAffairRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository
from domain.tasks.ports.task_repository import InMemoryTaskRepository, AbstractTaskRepository


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
def tag_in_memory_repo() -> AbstractTagRepository:
    tag_repo = InMemoryTagRepository()
    tag_repo._tags = []
    return tag_repo


@pytest.fixture(scope="function")
def task_in_memory_repo() -> AbstractTaskRepository:
    task_repo = InMemoryTaskRepository()
    task_repo._tasks = []
    return task_repo


@pytest.fixture(scope="session")
def tag_pg_repo(sqlite_engine: Engine) -> AbstractTagRepository:
    clear_mappers()
    start_mappers()
    tag_repository = PgTagRepository(sessionmaker(bind=sqlite_engine, autoflush=False)())
    return tag_repository


@pytest.fixture(scope="session")
def task_pg_repo(sqlite_engine: Engine, tag_pg_repo: AbstractTagRepository) -> AbstractTaskRepository:
    clear_mappers()
    start_mappers()
    task_repository = PgTaskRepository(sessionmaker(bind=sqlite_engine)())
    return task_repository


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # ,
def tag_repo(request, tag_in_memory_repo, tag_pg_repo) -> AbstractTagRepository:
    if request.param == "sqlite":
        repo = tag_pg_repo
    else:  # request.param == "in_memory"
        repo = tag_in_memory_repo
        repo._tags = []
    return repo


@pytest.fixture(scope="function", params=["in_memory", "sqlite"])  # , "sqlite"
def task_repo(request, task_in_memory_repo, task_pg_repo) -> AbstractTaskRepository:
    if request.param == "sqlite":
        repo = task_pg_repo
    else:  # request.param == "in_memory"
        repo = task_in_memory_repo
        repo._tasks = []
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
