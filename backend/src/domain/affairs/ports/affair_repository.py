import abc
from typing import List

from domain.affairs.entities.affair_entity import AffairEntity

affairsList = List[AffairEntity]


class AlreadyExistingAffairUuid(Exception):
    pass


class NotFoundAffair(Exception):
    pass


class AbstractAffairRepository(abc.ABC):

    def _add(self, entity: AffairEntity):
        raise NotImplementedError

    def get_one(self) -> AffairEntity:
        raise NotImplementedError

    def get_many(self, N) -> List[AffairEntity]:
        raise NotImplementedError

    def get_by_uuid(self, uuid: str) -> AffairEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundAffair
        return matches[0]

    @abc.abstractclassmethod
    def get_all(self) -> affairsList:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _match_uuid(self, uuid: str) -> List[AffairEntity]:
        raise NotImplementedError


class InMemoryAffairRepository(AbstractAffairRepository):
    _affairs: affairsList = []

    def _add(self, entity: AffairEntity):
        self._affairs.append(entity)

    def get_all(self) -> affairsList:
        return self._affairs

    def _match_uuid(self, uuid: str) -> List[AffairEntity]:
        return [affair for affair in self._affairs if affair.distributionID == uuid]

    # next methods are only for test purposes
    @property
    def affairs(self) -> affairsList:
        return self._affairs

    def set_affairs(self, affairs: affairsList) -> None:
        self._affairs = affairs
