import abc
from typing import List, Union
import xml.dom.minidom

from werkzeug.exceptions import HTTPException

from domain.affairs.cisu import EdxlEntity
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
        if self._match_uuid(affair.uuid):
            raise AlreadyExistingAffairUuid()
        self._add(affair)
        event_bus.publish(events.AffairCreatedEvent(data=affair))

    def get_one(self) -> AffairEntity:
        return self.get_all()[0]

    def get_many(self, n: int) -> List[AffairEntity]:
        return self.get_all()[0:n]

    def get_by_uuid(self, uuid: str) -> AffairEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundAffair
        return match

    @abc.abstractmethod
    def _add(self, entity: AffairEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> affairsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[AffairEntity,None]:
        raise NotImplementedError

    @staticmethod
    def build_affair_from_xml_string(xml_string: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parseString(xml_string)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity.from_create_event(edxl_message.resource.message.choice)

    @staticmethod
    def build_affair_from_xml_file(xml_path: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parse(xml_path)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())


class InMemoryAffairRepository(AbstractAffairRepository):
    _affairs: affairsList = []

    def _add(self, entity: AffairEntity):
        self._affairs.append(entity)

    def get_all(self) -> affairsList:
        return self._affairs

    def _match_uuid(self, uuid: str) -> Union[AffairEntity,None]:
        matches = [affair for affair in self._affairs if affair.uuid == uuid]
        if matches:
            return matches[0]
        else:
            return None

    @property
    def affairs(self) -> affairsList:
        return self._affairs

    def set_affairs(self, affairs: affairsList) -> None:
        self._affairs = affairs
