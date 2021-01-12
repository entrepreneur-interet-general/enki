import abc
from typing import Dict

from adapters.elasticsearch.affair_repository import ElasticAffairRepository
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.messages.ports.tag_repository import AbstractTagRepository
from elasticsearch import Elasticsearch


class ElasticRepositories:
    name = "ELASTIC"

    def __init__(self, config):
        super().__init__(config)
        self.client = Elasticsearch(config.ELASTIC_HOST, http_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD))
        self.affair = ElasticAffairRepository(client=self.client)

    def _reset(self):
        for index in self.client.indices.get_alias("*"):
            self.client.indices.delete(index=index, ignore=[400, 404])