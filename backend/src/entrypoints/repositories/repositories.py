import abc
from typing import Dict

from adapters.postgres.orm import metadata
from adapters.postgres.pg_affair_repository import PgAffairRepository
from adapters.random.random_cisu_repository import RandomCisuRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository, InMemoryAffairRepository
from domain.affairs.ports.message_repository import AbstractSgeMessageRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, InMemoryTaskRepository
from entrypoints.repositories.factories import get_pg_repos, build_engine


class Repositories(abc.ABC):
    name: str
    task: AbstractTaskRepository
    tag: AbstractTagRepository
    message: AbstractSgeMessageRepository
    affair: AbstractAffairRepository

    def __init__(self, config):
        self.config = config

    def init_app(self, app):
        app.context = self

    def reset(self):
        self._reset()

    @abc.abstractmethod
    def _reset(self):
        raise NotImplementedError


class InMemoryRepository(Repositories):
    name = "IN_MEMORY"

    def __init__(self, config) -> None:
        super().__init__(config)
        self.tag = InMemoryTagRepository()
        self.task = InMemoryTaskRepository(tag_repo=self.tag)
        self.affair = InMemoryAffairRepository()  # XmlCisuRepository()

    def _reset(self):
        """
        For test purpose

        :return:
        """
        self.tag._tags = []
        self.task._tasks = []


class SQLRepository(Repositories):
    name = "SQL"

    def __init__(self, config):
        super().__init__(config)
        self.engine = build_engine(sql_engine_uri=config.DATABASE_URI)
        self.tag, self.task, self.affair = get_pg_repos(engine=self.engine)

    def _reset(self):
        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)


REPOSITORY_TYPES: Dict[str, Repositories] = {
    SQLRepository.name: SQLRepository,
    InMemoryRepository.name: InMemoryRepository
}
