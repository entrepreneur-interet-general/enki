import abc
import os
import pathlib
from typing import List, Union, Any

from flask import current_app
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

from domain.messages.entities.resource import ResourceEntity

ResourcesList = List[ResourceEntity]


class AlreadyExistingResource(HTTPException):
    code = 409
    description = "Resource content already exists"


class NotFoundResource(HTTPException):
    code = 404
    description = "Resource content not found"


class AbstractResourceContentRepository(abc.ABC):
    def retrieve(self, bucket: str, object_path: str):
        if self._exists(bucket, object_path):
            return self._retrieve(bucket=bucket, object_path=object_path)
        else:
            raise NotFoundResource

    def store(self, local_path: str, bucket: str, object_path: str, content_type: str):
        if not self._exists(bucket, object_path):
            return self._store(local_path=local_path, bucket=bucket, object_path=object_path, content_type=content_type)
        else:
            raise AlreadyExistingResource

    def remove(self, resource: ResourceEntity):
        if self._exists(resource.bucket_name, resource.path_without_bucket):
            return self._remove(resource.bucket_name, resource.path_without_bucket)
        else:
            raise NotFoundResource

    @abc.abstractmethod
    def _store(self, local_path: str, bucket: str, object_path: str, content_type: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve(self, bucket: str, object_path: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _remove(self, bucket: str, object_path: str):
        raise NotImplementedError

    @abc.abstractmethod
    def _exists(self, bucket: str, object_path: str) -> bool:
        raise NotImplementedError


class LocalResourceContentRepository(AbstractResourceContentRepository):

    def _store(self,  local_path: str, bucket: str, object_path: str, content_type: str) -> None:
        filename = secure_filename(local_path)
        destination_path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) + filename
        source_path = pathlib.Path(local_path)
        with source_path.open('rb') as file:
            with destination_path.open('wb') as destination_file:
                destination_file.write(file.read())

    def _retrieve(self, bucket: str, object_path: str):
        path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) / object_path
        with path.open('rb') as source_file:
            return source_file.read()

    def _remove(self, bucket: str, object_path: str):
        path = pathlib.Path(current_app.config['UPLOAD_FOLDER']) / object_path
        path.unlink()

    def _exists(self, bucket: str, object_path: str) -> bool:
        p = pathlib.Path(current_app.config['UPLOAD_FOLDER']) / object_path
        if p.is_file():
            return True
        return False
