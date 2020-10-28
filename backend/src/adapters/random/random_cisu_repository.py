import random
from typing import List
import logging

from domain.affairs.cisu.factories.edxl_factory import AffairEntityFactory
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList


class RandomCisuRepository(AbstractAffairRepository):

    def __init__(self):
        self.all_affairs: List[AffairEntity] = []
        self.factory = AffairEntityFactory()
        self.all_affairs.extend(self.build_many(n=50))

    def _add(self, entity: AffairEntity):
        self.all_affairs.append(entity)

    def get_one(self) -> AffairEntity:
        return random.sample(self.all_affairs, 1)[0]

    def build_many(self, n) -> List[AffairEntity]:
        return [self.build_one() for _ in range(n)]

    def get_many(self, n) -> List[AffairEntity]:
        return random.sample(self.all_affairs, n)

    def get_all(self) -> affairsList:
        logging.info(f"self.all_affairs {self.all_affairs}")
        return self.all_affairs

    def _match_uuid(self, uuid: str) -> AffairEntity:
        _matches = [affair for affair in self.all_affairs if affair.distributionID == uuid]
        if _matches:
            return _matches[0]

    def build_one(self):
        return self.factory.build()