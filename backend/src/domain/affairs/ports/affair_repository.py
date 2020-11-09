import abc
from typing import List
import xml.dom.minidom
from uuid import uuid4

from werkzeug.exceptions import HTTPException

from domain.affairs.entities.affair_entity import AffairEntity
from entrypoints.extensions import event_bus, clock
from domain.core import events
affairsList = List[AffairEntity]


class AlreadyExistingAffairUuid(HTTPException):
    code = 409
    description = "test"
    message = "ok"


class NotFoundAffair(HTTPException):
    code = 404
    description = "test"
    message = "ok"


class AbstractAffairRepository(abc.ABC):

    def add(self, affair: AffairEntity) -> None:
        if self._match_uuid(affair.distributionID):
            raise AlreadyExistingAffairUuid()
        self._add(affair)
        event_bus.publish(events.AffairCreatedEvent(data=affair))

    def get_one(self) -> AffairEntity:
        return self.get_all()[0]

    def get_many(self, n: int) -> List[AffairEntity]:
        return self.get_all()[0:n]

    def get_by_uuid(self, uuid: str) -> AffairEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundAffair
        return matches[0]

    @abc.abstractmethod
    def _add(self, entity: AffairEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> affairsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> List[AffairEntity]:
        raise NotImplementedError

    @staticmethod
    def build_affair_from_xml_string(xml_string: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parseString(xml_string)
        return AffairEntity.from_xml(affair_dom)

    @staticmethod
    def build_affair_from_xml_file(xml_path: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parse(xml_path)
        return AffairEntity.from_xml(affair_dom)


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
