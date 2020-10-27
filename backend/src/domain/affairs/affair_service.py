from typing import Any, Dict, List
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository


def list_affairs(repo: AbstractAffairRepository) -> List[Dict[str, Any]]:
    affairs: List[AffairEntity] = repo.get_all()
    serialized_affairs = [affair.to_dict() for affair in affairs]
    return serialized_affairs


def get_by_uuid(uuid: str, repo: AbstractAffairRepository) -> Dict[str, Any]:
    affair: AffairEntity = repo.get_by_uuid(uuid)
    return affair.to_dict()

def get_random_affair(repo: AbstractAffairRepository)-> Dict[str, Any]:
    affair: AffairEntity = repo.get_one()
    return affair.to_dict()

def get_random_list_affairs(repo: AbstractAffairRepository, N=100)-> Dict[str, Any]:
    affair: AffairEntity = repo.get_many(N)
    return affair.to_dict()
