from datetime import timedelta
from typing import Union

from minio import Minio
from minio.api import Object
from flask import current_app
from urllib3 import HTTPResponse
from urllib3.exceptions import MaxRetryError

from domain.messages.entities.resource import ResourceEntity
from domain.messages.ports.resource_content_repository import AbstractResourceContentRepository


class ClientNotInitializedError(Exception):
    pass


class MinioResourceContentRepository(AbstractResourceContentRepository):
    """

    """

    @classmethod
    def from_config(cls, config):
        return cls(minio_uri=config.MINIO_URI,
                   access_key=config.MINIO_ACCESS_KEY,
                   secret_key=config.MINIO_SECRET_KEY,
                   bucket_list=[
                       config.MINIO_MESSAGE_RESOURCES_BUCKET
                   ])

    def __init__(self, minio_uri: str, access_key: str, secret_key: str, bucket_list: Union[list, None] = None):
        self.bucket_list = bucket_list or []
        try:
            self.client = Minio(minio_uri,
                                access_key=access_key,
                                secret_key=secret_key, secure=False)
            self.initialize()
        except MaxRetryError:
            self.client = None

    def initialize(self):
        for bucket in self.bucket_list:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

    def _store(self, local_path: str, bucket: str, object_path: str, content_type: str) -> None:
        if self.client:
            self.client.fput_object(bucket_name=bucket,
                                    object_name=object_path,
                                    file_path=local_path,
                                    content_type=content_type)
        else:
            raise ClientNotInitializedError

    def _retrieve(self, bucket: str, object_path: str) -> HTTPResponse:
        if self.client:
            return self.client.get_object(
                bucket_name=bucket,
                object_name=object_path,
            )
        else:
            raise ClientNotInitializedError

    def _exists(self, bucket: str, object_path: str) -> bool:
        stats = self.client.stat_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        if stats:
            return True
        else:
            return False

    def _remove(self, bucket: str, object_path: str):
        if self.client:
            self.client.remove_object(bucket, object_path)
        else:
            raise ClientNotInitializedError

    def list_objects(self, bucket: str, path: str):
        if self.client:
            objects = self.client.list_objects(bucket=bucket, prefix=path)
            return objects
        else:
            raise ClientNotInitializedError

    def get_presigned_get_url(self, bucket: str, object_path: str) -> str:
        url = self.client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        return url

    def get_presigned_put_url(self, bucket: str, object_path: str) -> str:
        url = self.client.presigned_put_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        return url
