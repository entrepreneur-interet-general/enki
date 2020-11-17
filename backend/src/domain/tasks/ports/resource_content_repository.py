import abc
import os
import pathlib
from typing import List, Union, Any

from flask import current_app
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from domain.tasks.entities.resource_entity import ResourceEntity, ResourceURI

ResourcesList = List[ResourceEntity]


class AlreadyExistingResource(HTTPException):
    code = 409
    description = "Resource already exists"


class NotFoundResource(HTTPException):
    code = 404
    description = "Resource not found"


class AbstractResourceContentRepository(abc.ABC):
    def retrieve(self, resource: ResourceEntity) -> Union[ResourceEntity, None]:
        if self._exists(resource.uri):
            return self._retrieve(resource.uri)
        else:
            raise NotFoundResource

    def store(self, local_path: str, resource: ResourceEntity):
        if not self._exists(resource.uri):
            return self._store(local_path=local_path, resource=resource)
        else:
            raise AlreadyExistingResource

    def remove(self, resource: ResourceEntity):
        if self._exists(resource.uri):
            return self._remove(resource.uri)
        else:
            raise NotFoundResource

    @abc.abstractmethod
    def _store(self, local_path: str, resource: ResourceEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve(self, path: ResourceURI):
        raise NotImplementedError

    @abc.abstractmethod
    def _remove(self, path: ResourceURI):
        raise NotImplementedError

    @abc.abstractmethod
    def _exists(self, path: ResourceURI) -> bool:
        raise NotImplementedError


class LocalResourceContentRepository(AbstractResourceContentRepository):

    def _store(self, local_path: str, resource: ResourceEntity) -> None:
        filename = secure_filename(resource.uri.path)
        destination_path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) + filename
        source_path = pathlib.Path(local_path)
        with source_path.open('rb') as file:
            with destination_path.open('wb') as destination_file:
                destination_file.write(file.read())

    def _retrieve(self, uri: ResourceURI):
        path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) + uri.path
        with path.open('rb') as source_file:
            return source_file.read()

    def _remove(self, path: ResourceURI):
        path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) + path.path
        path.unlink()

    def _exists(self, path: ResourceURI) -> bool:
        p = pathlib.Path(current_app.config['UPLOAD_FOLDER']) + path.path
        if p.is_file():
            return True
        return False
