import abc
from typing import List, Union
from werkzeug.exceptions import HTTPException

from domain.users.entities.group import GroupEntity

GroupsList = List[GroupEntity]


class AlreadyExistingGroupUuid(HTTPException):
    code = 409
    description = "Cet group existe déjà"


class NotFoundGroup(HTTPException):
    code = 404
    description = "Cet group n'existe pas"


class AbstractGroupRepository(abc.ABC):
    def get_by_uuid(self, uuid: str) -> GroupEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundGroup
        return matches

    @abc.abstractmethod
    def get_all(self) -> GroupsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[GroupEntity, None]:
        raise NotImplementedError


class InMemoryGroupRepository(AbstractGroupRepository):
    _groups: GroupsList = []

    def get_all(self) -> GroupsList:
        return self._groups

    def _match_uuid(self, uuid: str) -> Union[GroupEntity, None]:
        matches = [group for group in self._groups if group.uuid == uuid]
        if matches:
            return matches[0]
