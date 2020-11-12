import json

from elasticsearch import Elasticsearch, helpers

from typing import List, Union

from adapters.elasticsearch.base_repo import ElasticRepositoryMixin
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from elasticsearch.exceptions import NotFoundError

from entrypoints.serializers import SapeurJsonEncoder


class ElasticAffairRepository(ElasticRepositoryMixin, AbstractAffairRepository):

    def __init__(self, client: Elasticsearch):
        ElasticRepositoryMixin.__init__(self, client=client, index_name="affairs")
        AbstractAffairRepository.__init__(self)

    def create_indice(self):
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(self.index_name)

    def _match_uuid(self, uuid: str) -> Union[AffairEntity,None]:
        try:
            return AffairEntity(**self.client.get(index=self.index_name, id=uuid)["_source"])
        except NotFoundError as e:
            return None

    def _add(self, affair: AffairEntity) -> bool:
        return self.client.index(index=self.index_name, id=affair.uuid, body=json.dumps(affair.to_dict(), cls=SapeurJsonEncoder,))

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

