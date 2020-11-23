from typing import Any, Dict, List

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository


class AffairService:
    @staticmethod
    def add_affair(xml_string: str, repo: AbstractAffairRepository):
        affair: AffairEntity = repo.build_affair_from_xml_string(xml_string=xml_string)
        repo.add(affair)

    @staticmethod
    def get_by_uuid(uuid: str, repo: AbstractAffairRepository):
        return repo.get_by_uuid(uuid=uuid).to_dict()

    @staticmethod
    def list_affairs(repo: AbstractAffairRepository) -> List[Dict[str, Any]]:
        affairs: List[AffairEntity] = repo.get_all()
        serialized_affairs = [affair.to_dict() for affair in affairs]
        return serialized_affairs

    @staticmethod
    def get_random_affair(repo: AbstractAffairRepository) -> Dict[str, Any]:
        affair: AffairEntity = repo.get_one()
        return affair.to_dict()

    @staticmethod
    def get_random_list_affairs(repo: AbstractAffairRepository, n=10) -> List[Dict[str, Any]]:
        affairs: List[AffairEntity] = repo.get_many(n)
        return [affair.to_dict() for affair in affairs]
