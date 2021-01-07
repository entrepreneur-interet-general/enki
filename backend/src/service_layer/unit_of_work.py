import abc

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from adapters.postgres import PgTaskRepository, PgTagRepository, PgInformationRepository, PgEvenementRepository
from adapters.postgres.orm import metadata
from domain.affairs.ports.affair_repository import AbstractAffairRepository, InMemoryAffairRepository
from domain.evenements.repository import AbstractEvenementRepository, InMemoryEvenementRepository
from domain.tasks.ports import AbstractInformationRepository, AbstractTagRepository, AbstractTaskRepository
from domain.tasks.ports.information_repository import InMemoryInformationRepository
from domain.tasks.ports.tag_repository import InMemoryTagRepository
from domain.tasks.ports.task_repository import InMemoryTaskRepository
from entrypoints.repositories.repositories import ElasticRepositories


class AbstractUnitOfWork(abc.ABC):
    tag: AbstractTagRepository
    task: AbstractTaskRepository
    information: AbstractInformationRepository
    evenement: AbstractEvenementRepository
    affair: AbstractAffairRepository

    def __enter__(self):
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()  # (1)
        else:
            self.rollback()  # (2)

    def init_app(self, app):
        app.context = self

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError


def build_engine(sql_engine_uri: str) -> Engine:
    isolation_level = "READ UNCOMMITTED" if "sqlite" in sql_engine_uri else "REPEATABLE READ"
    engine = create_engine(
        sql_engine_uri,
        isolation_level=isolation_level,
    )
    return engine


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, config):
        self.engine = build_engine(sql_engine_uri=config.DATABASE_URI)
        self.session_factory = sessionmaker(bind=self.engine)
        metadata.create_all(self.engine)

        if config.AFFAIR_REPOSITORY == "ELASTIC":
            self.elastic_repositories = ElasticRepositories(config=config)
            self.affair = self.elastic_repositories.affair
        else:
            self.affair = InMemoryAffairRepository()

    def __enter__(self):
        self.session = self.session_factory()
        self.tag = PgTagRepository(self.session)
        self.task = PgTaskRepository(self.session)
        self.information = PgInformationRepository(self.session)
        self.evenement = PgEvenementRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()  # (3)

    def commit(self):  # (4)
        self.session.commit()

    def rollback(self):  # (4)
        self.session.rollback()

    def reset(self):
        self.tag.reset()
        self.task.reset()


class InMemoryUnitOfWork(AbstractUnitOfWork):

    def __init__(self, config):
        self.config = config
        self.tag = InMemoryTagRepository()
        self.task = InMemoryTaskRepository()
        self.information = InMemoryInformationRepository()
        self.evenement = InMemoryEvenementRepository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit(self):  # (4)
        pass

    def rollback(self):  # (4)
        pass

    def reset(self):
        self.tag.reset()
        self.task.reset()
