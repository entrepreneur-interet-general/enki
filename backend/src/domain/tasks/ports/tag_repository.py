import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.tasks.entities.tag_entity import TagEntity

TagsList = List[TagEntity]


class AlreadyExistingTagUuid(HTTPException):
    code = 409
    description = "Tag already exists"


class NotFoundTag(HTTPException):
    code = 404
    description = "Tag not found"


class AbstractTagRepository(abc.ABC):
    def add(self, tag: TagEntity) -> None:
        if self._match_uuid(tag.uuid):
            raise AlreadyExistingTagUuid()
        self._add(tag)

    def get_by_uuid(self, uuid: str) -> TagEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundTag
        return matches

    def get_by_uuid_list(self, uuids: List[str]) -> List[TagEntity]:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundTag
        return matches

    @abc.abstractmethod
    def get_all(self) -> TagsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[TagEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> List[TagEntity]:
        raise NotImplementedError


class InMemoryTagRepository(AbstractTagRepository):
    _tags: TagsList = []

    def get_all(self) -> TagsList:
        return self._tags

    def _match_uuid(self, uuid: str) -> Union[TagEntity, None]:
        matches = [tag for tag in self._tags if tag.uuid == uuid]
        if not matches:
            return None
        return matches[0]

    def _add(self, tag: TagEntity) -> None:
        self._tags.append(tag)

    def _match_uuids(self, uuids: List[str]) -> List[TagEntity]:
        matches = [tag for tag in self._tags if tag.uuid in uuids]
        return matches

    # next methods are only for test purposes
    @property
    def tags(self) -> TagsList:
        return self._tags

    def set_tags(self, tags: TagsList) -> None:
        self._tags = tags
