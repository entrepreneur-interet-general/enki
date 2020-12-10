import abc
from typing import List, Union
import xml.dom.minidom

from werkzeug.exceptions import HTTPException

from domain.evenements.entity import EvenementEntity

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

evenementsList = List[EvenementEntity]


class AlreadyExistingEvenementUuid(HTTPException):
    code = 409
    description = "Cet évenement existe déjà"


class NotFoundEvenement(HTTPException):
    code = 404
    description = "Cet évenement n'existe pas"


class AbstractEvenementRepository(abc.ABC):
    def add(self, event: EvenementEntity) -> Union[bool, None]:
        if self._match_uuid(event.uuid):
            raise AlreadyExistingEvenementUuid()
        result = self._add(event)
        return result

    def get_by_uuid(self, uuid: str) -> EvenementEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundEvenement
        return matches

    @abc.abstractmethod
    def _add(self, entity: EvenementEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> evenementsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[EvenementEntity, None]:
        raise NotImplementedError


class InMemoryEvenementRepository(AbstractEvenementRepository):
    _evenements: evenementsList = []

    def _add(self, entity: EvenementEntity):
        self._evenements.append(entity)

    def get_all(self) -> evenementsList:
        return self._evenements

    def _match_uuid(self, uuid: str) -> Union[EvenementEntity, None]:
        matches = [event for event in self._evenements if event.uuid == uuid]
        if matches:
            return matches[0]

    # next methods are only for test purposes
    @property
    def evenements(self) -> evenementsList:
        return self._evenements

    def set_evenements(self, evenements: evenementsList) -> None:
        self._evenements = evenements