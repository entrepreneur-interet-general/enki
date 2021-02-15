import abc
from typing import List, Union
from werkzeug.exceptions import HTTPException

from domain.users.entities.contact import ContactEntity
from domain.users.entities.user import UserEntity

UsersList = List[UserEntity]


class AlreadyExistingUserUuid(HTTPException):
    code = 409
    description = "Cet user existe déjà"

    def __init__(self, uuid):
        super(AlreadyExistingUserUuid, self).__init__()
        self.description = f"Cet user {uuid} existe déjà"


class NotFoundUser(HTTPException):
    code = 404
    description = "Cet user n'existe pas"

    def __init__(self, uuid):
        super(NotFoundUser, self).__init__()
        self.description = f"Cet user {uuid} n'existe pas"


class AbstractUserRepository(abc.ABC):
    def add(self, user: UserEntity) -> UserEntity:
        if self._match_uuid(user.uuid):
            raise AlreadyExistingUserUuid(uuid=user.uuid)
        _ = self._add(user)
        return user

    def get_by_uuid(self, uuid: str) -> UserEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundUser(uuid=uuid)
        return matches



    def get_user_contacts(self, uuid: str):
        user: UserEntity = self.get_by_uuid(uuid=uuid)
        return self._get_user_contacts(user)

    def get_user_contact(self, uuid: str, contact: ContactEntity):
        user: UserEntity = self.get_by_uuid(uuid=uuid)
        return self._get_user_contact(user, contact=contact)

    def add_user_contact(self, uuid: str, contact: ContactEntity):
        user: UserEntity = self.get_by_uuid(uuid=uuid)
        self._add_user_contact(user=user, contact=contact)

    def remove_user_contact(self, uuid: str, contact: ContactEntity):
        user: UserEntity = self.get_by_uuid(uuid=uuid)
        self._remove_user_contact(user=user, contact=contact)

    @abc.abstractmethod
    def _get_user_contacts(self, user: UserEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_user_contact(self, user: UserEntity, contact: ContactEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _add_user_contact(self, user: UserEntity, contact: ContactEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _remove_user_contact(self, user: UserEntity, contact: ContactEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, entity: UserEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> UsersList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[UserEntity, None]:
        raise NotImplementedError

class InMemoryUserRepository(AbstractUserRepository):
    _users: UsersList = []

    def _add(self, entity: UserEntity):
        self._users.append(entity)

    def get_all(self) -> UsersList:
        return self._users

    def _match_uuid(self, uuid: str) -> Union[UserEntity, None]:
        matches = [user for user in self._users if user.uuid == uuid]
        if matches:
            return matches[0]

    # next methods are only for test purposes
    @property
    def users(self) -> UsersList:
        return self._users

    def set_Users(self, users: UsersList) -> None:
        self._users = users