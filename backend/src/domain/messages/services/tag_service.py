from typing import Any, Dict, List
from domain.messages.entities.tag_entity import TagEntity
from domain.messages.ports.tag_repository import AbstractTagRepository
from domain.messages.schema import TagSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class TagService:
    schema = TagSchema

    @staticmethod
    def add_tag(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        tag: TagEntity = TagService.schema().load(data)
        return_value = TagService.schema().dump(tag)

        with uow:
            uow.tag.add(tag)
        return return_value

    @staticmethod
    def list_tags(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            tags: List[TagEntity] = uow.tag.get_all()
            return TagService.schema(many=True).dump(tags)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag = uow.tag.get_by_uuid(uuid)
            return TagService.schema().dump(tag)
