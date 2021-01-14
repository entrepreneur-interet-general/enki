import json

from elasticsearch import Elasticsearch, helpers

from typing import List, Union

from adapters.elasticsearch.base_repo import ElasticRepositoryMixin
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList
from elasticsearch.exceptions import NotFoundError

from entrypoints.serializers import EnkiJsonEncoder


class ElasticAffairRepository(ElasticRepositoryMixin, AbstractAffairRepository):

    def __init__(self, client: Elasticsearch, index_name="affairs"):
        ElasticRepositoryMixin.__init__(self, client=client, index_name=index_name)
        AbstractAffairRepository.__init__(self)
        self.create_indice()

    def _match_uuid(self, uuid: str) -> Union[AffairEntity, None]:
        try:
            return AffairEntity(**self.client.get(index=self.index_name, id=uuid)["_source"])
        except NotFoundError as e:
            return None

    def _get_from_polygon(self, multipolygon: List) -> affairsList:
        query = {
            "query": {
                "bool": {
                    "must": {
                        "match_all": {}
                    },
                    "filter": {
                        "geo_polygon": {
                            "location": {
                                "points": multipolygon
                            }
                        }
                    }
                }
            }
        }
        results = self.client.search(
            index=self.index_name,
            body=query
        )
        return self._map_es_results_with_affairs(results=results)

    def _add(self, affair: AffairEntity) -> bool:
        return self.client.index(index=self.index_name, id=affair.uuid,
                                 body=json.dumps(affair.to_dict(), cls=EnkiJsonEncoder, ),
                                 refresh=True, )

    def _bulk_add(self, affairs: List[AffairEntity]):
        actions = [
            {
                "_index": self.index_name,
                "_id": affair.uuid,
                "_source": affair.to_dict()
            } for affair in affairs
        ]

        return helpers.bulk(self.client, actions)

    def exists(self, uuid: str) -> bool:
        return self.client.get(index=self.index_name, id=uuid)

    def get_all(self) -> List[AffairEntity]:
        results = self.client.search(
            index=self.index_name,
            body={"query": {"match_all": {}}}
        )
        return self._map_es_results_with_affairs(results=results)

    def _match_uuids(self, uuids: List[str]) -> List[AffairEntity]:
        results = self.client.search(
            index=self.index_name,
            body={
                "query": {
                    "ids": {
                        "values": uuids
                    }
                }
            }
        )
        return self._map_es_results_with_affairs(results=results)

    @staticmethod
    def _map_es_results_with_affairs(results: dict):
        return [AffairEntity(**hit["_source"]) for hit in results['hits']['hits']]
