import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, clear_mappers

from adapters.postgres import PgTagRepository, PgTaskRepository
from adapters.postgres.orm import start_mappers, metadata
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
    #[table.drop(sqlite_engine) for table in all_tables]


@pytest.fixture(scope="function")
def tag_in_memory_repo() -> AbstractTagRepository:
    tag_repo = InMemoryTagRepository()
    tag_repo._tags = []
    return tag_repo


@pytest.fixture(scope="function")
def task_in_memory_repo(tag_repo: AbstractTagRepository) -> AbstractTaskRepository:
    task_repo = InMemoryTaskRepository(tag_repo=tag_repo)
    task_repo._tasks = []
    return task_repo


@pytest.fixture(scope="session")
def tag_pg_repo(sqlite_engine: Engine) -> AbstractTagRepository:
    clear_mappers()
    start_mappers(sqlite_engine)
    tag_repository = PgTagRepository(sessionmaker(bind=sqlite_engine, autoflush=False)())
    return tag_repository


@pytest.fixture(scope="session")
def task_pg_repo(sqlite_engine: Engine, tag_pg_repo: AbstractTagRepository) -> AbstractTaskRepository:
    clear_mappers()
    start_mappers(sqlite_engine)
    task_repository = PgTaskRepository(sessionmaker(bind=sqlite_engine)(), tag_repo=tag_pg_repo)
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
        repo._tasks = []
    else:  # request.param == "in_memory"
        repo = task_in_memory_repo
        repo._tasks = []
    return repo
