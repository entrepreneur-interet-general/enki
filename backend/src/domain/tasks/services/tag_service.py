from typing import Any, Dict, List
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.ports.tag_repository import AbstractTagRepository
from service_layer.unit_of_work import AbstractUnitOfWork


class TagService:

    @staticmethod
    def add_tag(uuid: str, title: str, uow: AbstractUnitOfWork, description: str = None, color: str = None, ):
        new_tag = TagEntity(uuid=uuid,
                            title=title,
                            description=description,
                            color=color)
        with uow:
            uow.tag.add(new_tag)

    @staticmethod
    def list_tags(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            tags: List[TagEntity] = uow.tag.get_all()
            serialized_tags = [tag.to_dict() for tag in tags]
            return serialized_tags

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag = uow.tag.get_by_uuid(uuid)
            return tag.to_dict()
