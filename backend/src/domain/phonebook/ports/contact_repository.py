import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.phonebook.entities.contact import ContactEntity

ContactsList = List[ContactEntity]


class AlreadyExistingContactUuid(HTTPException):
    code = 409
    description = "Contact already exists"


class NotFoundContact(HTTPException):
    code = 404
    description = "Contact not found"


class AbstractContactRepository(abc.ABC):
    def add(self, contact: ContactEntity) -> None:
        if self._match_uuid(contact.uuid):
            raise AlreadyExistingContactUuid()
        self._add(contact)
        # TODO : test if title already exists

    def get_by_uuid(self, uuid: str) -> ContactEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundContact
        return matches

    def get_by_uuid_list(self, uuids: List[str]) -> List[ContactEntity]:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundContact
        return matches

    @abc.abstractmethod
    def get_all(self) -> ContactsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, contact: ContactEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[ContactEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> List[ContactEntity]:
        raise NotImplementedError
