import abc
import json
import pathlib
from http.client import HTTPException
from typing import List, Any

from elasticsearch import Elasticsearch


class NotFoundException(HTTPException):
    code = 404


class ElasticRepositoryMixin(abc.ABC):
    def __init__(self, client: Elasticsearch, index_name: str):
        self.client: Elasticsearch = client
        self.index_name: str = index_name
        self.create_indice()

    def create_indice(self):
        if not self.client.indices.exists(index=self.index_name):
            template_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()) / f"templates/{self.index_name}.json"
            with template_path.open() as f:
                template = json.load(f)
            self.client.indices.create(self.index_name, body=template)

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
