import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.info_entity import InformationEntity
from domain.tasks.ports.tag_repository import AbstractTagRepository

InformationsList = List[InformationEntity]


class AlreadyExistingInformationUuid(HTTPException):
    code = 409
    description = "Information already exists"


class NotFoundInformation(HTTPException):
    code = 404
    description = "Information not found"


class AlreadyExistingTagInThisInformation(HTTPException):
    code = 409
    description = "Tag already exists in this information"


class NotFoundTagInThisInformation(HTTPException):
    code = 404
    description = "Tag not found in this information"


class AbstractInformationRepository(abc.ABC):
    def add(self, information: InformationEntity) -> None:
        if self._match_uuid(information.uuid):
            raise AlreadyExistingInformationUuid()
        self._add(information)

    def get_by_uuid(self, uuid: str) -> InformationEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundInformation
        return match

    def get_tag_by_information(self, uuid: str, tag_uuid: str) -> TagEntity:
        match = self._get_tag_by_information(uuid=uuid, tag_uuid=tag_uuid)
        if not match:
            raise NotFoundTagInThisInformation
        return match

    def get_tags(self, uuid: str):
        match = self.get_by_uuid(uuid=uuid)
        if not match:
            raise NotFoundTagInThisInformation
        return match.tags

    @abc.abstractmethod
    def get_all(self) -> InformationsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, information: InformationEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[InformationEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tag_by_information(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        raise NotImplementedError


class InMemoryInformationRepository(AbstractInformationRepository):
    _informations: InformationsList = []

    def get_all(self) -> InformationsList:
        return self._informations

    def _match_uuid(self, uuid: str) -> Union[InformationEntity, None]:
        matches = [information for information in self._informations if information.uuid == uuid]
        if not matches:
            return None
        return matches[0]

    def _add(self, information: InformationEntity):
        self._informations.append(information)

    # next methods are only for test purposes
    @property
    def informations(self) -> InformationsList:
        return self._informations

    def set_informations(self, informations: InformationsList) -> None:
        self._informations = informations

    def add_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        information.tags.append(tag)

    def remove_tag_to_information(self, information: InformationEntity, tag: TagEntity) -> None:
        information.tags.remove(tag)

    def _get_tag_by_information(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        information: InformationEntity = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in information.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]
