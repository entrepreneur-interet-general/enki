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
        schema = ResourceService.schema()
        schema.context = {
            "bucket_name_config": uow.config.MINIO_MESSAGE_RESOURCES_BUCKET
        }
        resource: ResourceEntity = schema.load(data)
        return_value = schema.dump(resource)

        with uow:
            uow.resource.add(resource)

        return return_value

    @staticmethod
    def get_resource(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            resource: ResourceEntity = uow.resource.get_by_uuid(uuid)
            return_value = ResourceService.schema().dump(resource)

        return return_value

    @staticmethod
    def delete_resource(uuid: str, uow: AbstractUnitOfWork) -> bool:
        with uow:
            uow.resource.delete_by_uuid(uuid=uuid)
        return True
