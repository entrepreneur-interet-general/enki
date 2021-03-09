import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.evenements.entities.resource import ResourceEntity

ResourcesList = List[ResourceEntity]


class AlreadyExistingResourceUuid(HTTPException):
    code = 409
    description = "Resource already exists"


class NotFoundResource(HTTPException):
    code = 404
    description = "Resource not found"


class AbstractResourceRepository(abc.ABC):
    def add(self, resource: ResourceEntity) -> None:
        if self._match_uuid(resource.uuid):
            raise AlreadyExistingResourceUuid()
        self._add(resource)
        # TODO : test if title already exists

    def get_by_uuid(self, uuid: str) -> ResourceEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundResource
        return matches

    def delete_by_uuid(self, uuid: str) -> bool:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundResource
        return self._delete(matches)

    def get_by_uuid_list(self, uuids: List[str]) -> List[ResourceEntity]:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundResource
        return matches

    @abc.abstractmethod
    def get_all(self) -> ResourcesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, resource: ResourceEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, resource: ResourceEntity) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[ResourceEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> List[ResourceEntity]:
        raise NotImplementedError


class InMemoryResourceRepository(AbstractResourceRepository):
    _resources: ResourcesList = []

    def get_all(self) -> ResourcesList:
        return self._resources

    def _match_uuid(self, uuid: str) -> Union[ResourceEntity, None]:
        matches = [resource for resource in self._resources if resource.uuid == uuid]
        if not matches:
            return None
        return matches[0]

    def _add(self, resource: ResourceEntity) -> None:
        self._resources.append(resource)

    def _match_uuids(self, uuids: List[str]) -> List[ResourceEntity]:
        matches = [resource for resource in self._resources if resource.uuid in uuids]
        return matches

    def _delete(self, resource: ResourceEntity) -> bool:
        self._resources.remove(resource)
        return True

    # next methods are only for test purposes
    @property
    def resources(self) -> ResourcesList:
        return self._resources

    def set_resources(self, resources: ResourcesList) -> None:
        self._resources = resources
