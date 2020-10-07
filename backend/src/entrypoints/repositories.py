import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from adapters.postgres.orm import start_mappers
from adapters.postgres.pg_task_repository import PgTaskRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, InMemoryTaskRepository

def getPgRepos() -> AbstractTaskRepository:
    engine = create_engine(
        os.environ.get('SQLALCHEMY_ENGINE_OPTIONS', 'postgresql://postgres:pg-password@localhost:5432/sapeurs-dev'),
        isolation_level="REPEATABLE READ",
    )

    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()
    return PgTaskRepository(session)

class Repositories:
    task: AbstractTaskRepository

    def __init__(self) -> None:
        repo_infra = os.environ.get('REPOSITORIES')

        print("----   Repositories : ", repo_infra or 'IN MEMORY ' )

        if(repo_infra == 'PG'):
            self.task = getPgRepos()
        else:
            self.task = InMemoryTaskRepository()

