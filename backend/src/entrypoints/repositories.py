import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

from adapters.postgres.orm import start_mappers
from adapters.postgres.sge.orm import start_mappers as sge_mappers
from adapters.postgres.pg_task_repository import PgTaskRepository
from adapters.postgres.sge.pg_affairs_repository import PgSgeMessageRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, InMemoryTaskRepository
from domain.affairs.ports.message_repository import AbstractSgeMessageRepository, InMemorySgeMessageRepository
from adapters.xml.xml_cisu_repository import XmlCisuRepository
from adapters.random.random_cisu_repository import RandomCisuRepository

def getPgTaskRepos() -> AbstractTaskRepository:
    engine = create_engine(
        os.environ.get('SQLALCHEMY_ENGINE_OPTIONS', 'postgresql://postgres:pg-password@localhost:5432/sapeurs-dev'),
        isolation_level="REPEATABLE READ",
    )
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()
    return PgTaskRepository(session)


def getPgMessageRepos() -> AbstractSgeMessageRepository:
    sge_engine = create_engine(
        os.environ.get('SQLALCHEMY_SGE_ENGINE_OPTIONS'),
        isolation_level="REPEATABLE READ", echo = True
    )

    sge_mappers(engine=sge_engine)
    session_factory = sessionmaker(bind=sge_engine)
    session: Session = session_factory()
    return PgSgeMessageRepository(session)


class Repositories:
    task: AbstractTaskRepository

    def __init__(self) -> None:
        repo_infra = os.environ.get('REPOSITORIES')

        print("----   Repositories : ", repo_infra or 'IN MEMORY ')

        if repo_infra == 'PG':
            self.task = getPgTaskRepos()
            self.message = getPgMessageRepos()
        else:
            self.task = InMemoryTaskRepository()
            self.message = InMemorySgeMessageRepository()

        self.affairs = RandomCisuRepository() #XmlCisuRepository()
