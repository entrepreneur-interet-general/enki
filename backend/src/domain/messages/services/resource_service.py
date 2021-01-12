from tempfile import NamedTemporaryFile
from typing import Any, Dict, List
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from domain.messages.entities.resource import ResourceEntity
from domain.messages.schemas.resource_schema import ResourceSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class ResourceService:
    schema = ResourceSchema

    @staticmethod
    def add_resource(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        resource: ResourceEntity = ResourceService.schema().load(data)
        return_value = ResourceService.schema().dump(resource)

        with uow:
            uow.resource.add(resource)
        return return_value

    @staticmethod
    def upload_resource(data: dict, file: FileStorage, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        content_type = data["content_type"]
        uuid = str(uuid4())
        bucket_name = uow.config.MINIO_MESSAGE_RESOURCES_BUCKET
        with NamedTemporaryFile(mode="w") as f:
            file.save(f.name)
            with uow:
                uow.resource_content.store(local_path=f.name,
                                           bucket=bucket_name,
                                           object_path=uuid,
                                           content_type=content_type
                                           )
        return {
            "bucket_name": bucket_name,
            "object_path": uuid,
            "content_type": content_type,
            "original_name": file.filename,
        }

    @staticmethod
    def list_resources(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            resources: List[ResourceEntity] = uow.resource.get_all()
            return ResourceService.schema(many=True).dump(resources)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            resource = uow.resource.get_by_uuid(uuid)
            return ResourceService.schema().dump(resource)

    @staticmethod
    def load_content(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            resource = uow.resource_content.retrieve(bucket=uow.config.MINIO_MESSAGE_RESOURCES_BUCKET,
                                                     object_path=uuid)
            return resource
