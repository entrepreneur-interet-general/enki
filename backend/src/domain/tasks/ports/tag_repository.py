import abc
from typing import List, Union

from domain.tasks.entities.tag_entity import TagEntity

TagsList = List[TagEntity]


class AlreadyExistingTagUuid(Exception):
    pass


class NotFoundTag(Exception):
    pass


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

    @abc.abstractclassmethod
    def get_all(self) -> TagsList:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _add(self, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _match_uuid(self, uuid: str) -> Union[TagEntity, None]:
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

    # next methods are only for test purposes
    @property
    def tags(self) -> TagsList:
        return self._tags

    def set_tags(self, tags: TagsList) -> None:
        self._tags = tags
