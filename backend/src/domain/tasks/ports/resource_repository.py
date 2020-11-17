import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException
from domain.tasks.entities.resource_entity import ResourceEntity
from domain.tasks.ports.resource_content_repository import AbstractResourceContentRepository

ResourcesList = List[ResourceEntity]


class AlreadyExistingResourceUuid(HTTPException):
    code = 409
    description = "Resource already exists"


class NotFoundResource(HTTPException):
    code = 404
    description = "Resource not found"


class AbstractResourceRepository(abc.ABC):
    def __init__(self, content_repo: AbstractResourceContentRepository):
        self.content_repo = content_repo

    def add(self, local_path: str, resource: ResourceEntity) -> None:
        if self._match_uuid(resource.uuid):
            raise AlreadyExistingResourceUuid()
        self._add(resource)
        self._upload_file(local_path=local_path, resource=resource)

    def get_by_uuid(self, uuid: str) -> ResourceEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundResource
        return match

    def get_all(self) -> ResourcesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _upload_file(self, local_path: str, resource: ResourceEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_file(self, resource: ResourceEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, resource: ResourceEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[ResourceEntity, None]:
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

    def _add(self, resource: ResourceEntity):
        self._resources.append(resource)

    def _upload_file(self, local_path: str, resource: ResourceEntity):
        self.content_repo.store(local_path=local_path, resource=resource)

    def _delete_file(self, resource: ResourceEntity):
        self.content_repo.remove(resource=resource)

    # next methods are only for test purposes
    @property
    def resources(self) -> ResourcesList:
        return self._resources

    def set_resources(self, resources: ResourcesList) -> None:
        self._resources = resources
