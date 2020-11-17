from minio import Minio
from flask import current_app

from domain.tasks.entities.resource_entity import ResourceURI, ResourceEntity
from domain.tasks.ports.resource_content_repository import AbstractResourceContentRepository


class MinioResourceContentRepository(AbstractResourceContentRepository):
    """

    """

    def __init__(self, minio_uri: str, access_key: str, secret_key: str):
        self.client = Minio(minio_uri,
                            access_key=access_key,
                            secret_key=secret_key)

    def _store(self, local_path: str, resource: ResourceEntity) -> None:
        self.client.fput_object(bucket_name=resource.uri.bucket_name,
                                object_name=resource.uri.path_without_bucket,
                                file_path=local_path,
                                content_type=resource.content_type)

    def _retrieve(self, path: ResourceURI):
        pass

    def _remove(self, path: ResourceURI):
        self.client.remove_object(path.bucket_name, path.path_without_bucket)

    def _exists(self, path: ResourceURI) -> bool:
        pass
