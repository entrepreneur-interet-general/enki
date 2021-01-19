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
    def add_resource(data: Dict[str, Any], uow: AbstractUnitOfWork) -> str:
        schema = ResourceService.schema()
        schema.context = {
            "bucket_name_config": uow.config.MINIO_MESSAGE_RESOURCES_BUCKET
        }
        resource: ResourceEntity = schema.load(data)
        return_value = schema.dump(resource)

        with uow:
            uow.resource.add(resource)
            upload_url = uow.resource_content.get_presigned_put_url(
                bucket=uow.config.MINIO_MESSAGE_RESOURCES_BUCKET,
                object_path=resource.uuid
            )
            return_value["upload_url"] = upload_url

        return return_value

    @staticmethod
    def get_resource(uuid: str, uow: AbstractUnitOfWork) -> str:
        with uow:
            resource: ResourceEntity = uow.resource.get_by_uuid(uuid)
            download_url = uow.resource_content.get_presigned_get_url(bucket=uow.config.MINIO_MESSAGE_RESOURCES_BUCKET,
                                                                      object_path=resource.object_path)

            return_value = ResourceService.schema().dump(resource)
        return_value["url"] = download_url

        return return_value
