import abc
from typing import Dict

from adapters.elasticsearch.affair_repository import ElasticAffairRepository
from adapters.postgres.orm import metadata
from domain.affairs.ports.affair_repository import AbstractAffairRepository, InMemoryAffairRepository
from domain.evenements.repository import InMemoryEvenementRepository
from domain.messages.ports.tag_repository import AbstractTagRepository, InMemoryTagRepository
from entrypoints.repositories.factories import get_pg_repos, build_engine
from elasticsearch import Elasticsearch


class Repositories(abc.ABC):
    name: str
    tag: AbstractTagRepository
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


class InMemoryRepositories(Repositories):
    name = "IN_MEMORY"

    def __init__(self, config) -> None:
        super().__init__(config)
        self.tag = InMemoryTagRepository()
        self.affair = InMemoryAffairRepository()
        self.evenement = InMemoryEvenementRepository()

    def _reset(self):
        """
        For test purpose

        :return:
        """
        self.tag._tags = []
        self.task._tasks = []


class SQLRepositories(Repositories):
    name = "SQL"

    def __init__(self, config):
        super().__init__(config)
        self.engine = build_engine(sql_engine_uri=config.DATABASE_URI)
        self.tag, self.task, self.affair, self.evenement = get_pg_repos(engine=self.engine)

    def _reset(self):
        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)


class ElasticRepositories(Repositories):
    name = "ELASTIC"

    def __init__(self, config):
        super().__init__(config)
        self.client = Elasticsearch(config.ELASTIC_HOST, http_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD))
        self.affair = ElasticAffairRepository(client=self.client)

    def _reset(self):
        for index in self.client.indices.get_alias("*"):
            self.client.indices.delete(index=index, ignore=[400, 404])


class HybridRepositories(Repositories):

    name = "HYBRID"

    def __init__(self, config):
        super().__init__(config)
        self.in_memory_repositories = InMemoryRepositories(config=config)
        self.sql_repositories = SQLRepositories(config=config)
        self.elastic_repositories = ElasticRepositories(config=config)
        self.select_repositories()

    def select_repositories(self):
        self.affair = self.elastic_repositories.affair
        self.tag, self.task = self.in_memory_repositories.tag, self.in_memory_repositories.task
        self.evenement = self.in_memory_repositories.evenement
    def _reset(self):
        self.in_memory_repositories.reset()
        self.sql_repositories.reset()
        self.elastic_repositories.reset()


REPOSITORY_TYPES: Dict[str, Repositories] = {
    SQLRepositories.name: SQLRepositories,
    InMemoryRepositories.name: InMemoryRepositories,
    ElasticRepositories.name: ElasticRepositories,
    HybridRepositories.name: HybridRepositories
}
