import abc
from typing import Dict

from ...domain.elus.maires.repository import AbstractMaireRepository, InMemoryMaireRepository
from .factories import get_pg_repos, build_engine


class Repositories(abc.ABC):
    name: str
    maire: AbstractMaireRepository

    def __init__(self, config):
        self.config = config

    def init_app(self, app):
        app.context = self

class InMemoryRepositories(Repositories):
    name = "IN_MEMORY"

    def __init__(self, config) -> None:
        super().__init__(config)
        self.maire = InMemoryMaireRepository()


class SQLRepositories(Repositories):
    name = "SQL"

    def __init__(self, config):
        super().__init__(config)
        self.engine = build_engine(sql_engine_uri=config.DATABASE_URI)
        self.maire = get_pg_repos(engine=self.engine)


REPOSITORY_TYPES: Dict[str, Repositories] = {
    SQLRepositories.name: SQLRepositories,
    InMemoryRepositories.name: InMemoryRepositories,
}
