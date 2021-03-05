import abc
from typing import List, Union
from werkzeug.exceptions import HTTPException

from domain.evenements.entity import EvenementEntity, UserEvenementRole

evenementsList = List[EvenementEntity]


class AlreadyExistingEvenementUuid(HTTPException):
    code = 409
    description = "Cet évenement existe déjà"

class UserAlreadyAccessEvenement(HTTPException):
    code = 409
    description = "Cet utilisateur à déjà accès à cet évenement"

class NotFoundEvenement(HTTPException):
    code = 404
    description = "Cet évenement n'existe pas"


class AbstractEvenementRepository(abc.ABC):
    def add(self, event: EvenementEntity) -> EvenementEntity:
        if self._match_uuid(event.uuid):
            raise AlreadyExistingEvenementUuid()
        _ = self._add(event)
        return event

    def get_by_uuid(self, uuid: str) -> EvenementEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundEvenement
        return matches

    def add_user_role(self, user_role: UserEvenementRole):
        if self._match_user_event(user_role):
            raise UserAlreadyAccessEvenement()
        _ = self._add_user_role(user_role)
        return  user_role

    @abc.abstractmethod
    def _add(self, entity: EvenementEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _add_user_role(self, user_role: UserEvenementRole):
        raise NotImplementedError

    @abc.abstractmethod
    def _match_user_event(self, user_role: UserEvenementRole):
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