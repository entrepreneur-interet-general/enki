import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

from adapters.postgres.orm import start_mappers
from adapters.postgres import PgTaskRepository, PgTagRepository
from adapters.postgres.sge.orm import start_mappers as sge_mappers
from adapters.postgres.pg_task_repository import PgTaskRepository
from adapters.postgres.sge.pg_affairs_repository import PgSgeMessageRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, InMemoryTaskRepository
from domain.affairs.ports.message_repository import AbstractSgeMessageRepository, InMemorySgeMessageRepository
from adapters.xml.xml_cisu_repository import XmlCisuRepository
from domain.tags.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository
from adapters.random.random_cisu_repository import RandomCisuRepository


def getPgRepos() -> (AbstractTagRepository, AbstractTaskRepository):
    engine = create_engine(
        os.environ.get('SQLALCHEMY_ENGINE_OPTIONS', 'postgresql://postgres:pg-password@localhost:5432/sapeurs-dev'),
        isolation_level="REPEATABLE READ",
    )
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    session: Session = session_factory()

    return PgTagRepository(session), PgTaskRepository(session)



def getPgMessageRepos() -> AbstractSgeMessageRepository:
    sge_engine = create_engine(
        os.environ.get('SQLALCHEMY_SGE_ENGINE_OPTIONS'),
        isolation_level="REPEATABLE READ", echo=True
    )

    sge_mappers(engine=sge_engine)
    session_factory = sessionmaker(bind=sge_engine)
    session: Session = session_factory()
    return PgSgeMessageRepository(session)


class Repositories:
    task: AbstractTaskRepository
    tag: AbstractTagRepository

    def __init__(self) -> None:
        repo_infra: str = os.environ.get('REPOSITORIES')
        connect_to_sge: bool = os.environ.get('CONNECT_TO_SGE') == 'true'

        print("----   Repositories : ", repo_infra or 'IN MEMORY ')

        if repo_infra == 'PG':
            self.tag, self.task = getPgRepos()
        else:
            self.tag, self.task = InMemoryTagRepository(), InMemoryTaskRepository()

        if connect_to_sge:
            self.message = getPgMessageRepos()
        else:
            self.message = InMemorySgeMessageRepository()

        self.affairs = RandomCisuRepository()  # XmlCisuRepository()
