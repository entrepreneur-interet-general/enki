import glob
from typing import List
import xml.dom.minidom
import logging

from domain.affairs.cisu.factories.edxl_factory import AffairEntityFactory
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList
import pathlib


class RandomCisuRepository(AbstractAffairRepository):

    def __init__(self):
        self.all_affairs: List[AffairEntity] = []
        self.factory = AffairEntityFactory()

    def _add(self, entity: AffairEntity):
        self.all_affairs.append(entity)

    def get_one(self) -> AffairEntity:
        return self.build_one()

    def get_many(self, n) -> List[AffairEntity]:
        return [self.build_one() for _ in range(n)]

    def get_all(self) -> affairsList:
        logging.info(f"self.all_affairs {self.all_affairs}")
        return self.all_affairs

    def _match_uuid(self, uuid: str) -> AffairEntity:
        _matches = [affair for affair in self.all_affairs if affair.distributionID == uuid]
        if _matches:
            return _matches[0]

    @staticmethod
    def build_one():
        return self.factory.build()

    def build_n_affairs(self, N=100):
        self.all_affairs = [self.build_one() for _ in range(N)]