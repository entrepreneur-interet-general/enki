import abc

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from adapters.postgres import PgMessageRepository, PgTagRepository, PgEvenementRepository
from adapters.postgres.orm import metadata
from adapters.minio.resource_content_repository import MinioResourceContentRepository
from adapters.postgres.pg_resource_repository import PgResourceRepository
from adapters.postgres.pg_simple_affair_repository import PgSimpleAffairRepository
from adapters.postgres.pg_user_repository import PgUserRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository, InMemoryAffairRepository
from domain.affairs.ports.simple_affair_repository import AbstractSimpleAffairRepository
from domain.evenements.repository import AbstractEvenementRepository, InMemoryEvenementRepository
from domain.messages.ports import AbstractTagRepository, AbstractMessageRepository, AbstractResourceRepository
from domain.messages.ports.message_repository import InMemoryMessageRepository
from domain.messages.ports.tag_repository import InMemoryTagRepository
from domain.users.repository import AbstractUserRepository
from entrypoints.repositories import ElasticRepositories


class AbstractUnitOfWork(abc.ABC):
    resource: AbstractResourceRepository
    tag: AbstractTagRepository
    message: AbstractMessageRepository
    evenement: AbstractEvenementRepository
    affair: AbstractAffairRepository
    simple_affair: AbstractSimpleAffairRepository
    user: AbstractUserRepository

    def __init__(self, config):
        self.config = config

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
        super().__init__(config)
        self.engine = build_engine(sql_engine_uri=self.config.DATABASE_URI)
        self.session_factory = sessionmaker(bind=self.engine)
        metadata.create_all(self.engine)

        if config.AFFAIR_REPOSITORY == "ELASTIC":
            self.elastic_repositories = ElasticRepositories(config=self.config)
            self.affair = self.elastic_repositories.affair
        else:
            self.affair = InMemoryAffairRepository()

    def __enter__(self):
        self.session = self.session_factory()
        self.tag = PgTagRepository(self.session)
        self.message = PgMessageRepository(self.session)
        self.evenement = PgEvenementRepository(self.session)
        self.resource = PgResourceRepository(self.session)
        self.simple_affair = PgSimpleAffairRepository(self.session)
        self.user = PgUserRepository(self.session)
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
        super().__init__(config)
        self.config = config
        self.tag = InMemoryTagRepository()
        self.message = InMemoryMessageRepository()
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
