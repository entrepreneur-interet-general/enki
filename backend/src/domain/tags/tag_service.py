from typing import Any, Dict, List
from .entities.tag_entity import TagEntity
from .ports.tag_repository import AbstractTagRepository


class TagService:

    @staticmethod
    def add_tag(uuid: str, title: str, repo: AbstractTagRepository, description: str = None, color: str = None):
        new_tag = TagEntity(uuid=uuid, title=title, description=description, color=color)
        repo.add(new_tag)

    @staticmethod
    def list_tags(repo: AbstractTagRepository) -> List[Dict[str, Any]]:
        tags: List[TagEntity] = repo.get_all()
        serialized_tags = [tag.to_dict() for tag in tags]
        return serialized_tags

    @staticmethod
    def get_by_uuid(uuid: str, repo: AbstractTagRepository) -> Dict[str, Any]:
        tag = repo.get_by_uuid(uuid)
        return tag.to_dict()
