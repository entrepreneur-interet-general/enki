import abc
from http.client import HTTPException

from typing import List, Any
from elasticsearch import Elasticsearch


class NotFoundException(HTTPException):
    code = 404


class ElasticRepositoryMixin(abc.ABC):
    def __init__(self, client: Elasticsearch, index_name: str):
        self.client: Elasticsearch = client
        self.index_name: str = index_name

    def __add(self, doc: dict, uuid: str) -> bool:
        return self.client.index(index=self.index_name, id=uuid, body=doc)

    def _match_uuid(self, uuid: str) -> dict:
        return self.client.get(index=self.index_name, id=uuid)

    def _exists(self, uuid: str) -> bool:
        return self.client.get(index=self.index_name, id=uuid)

    def get_all(self) -> List[Any]:
        results = self.client.search(
            index=self.index_name,
            body={"query": {"match_all": {}}}
        )
        return results['hits']['hits']
