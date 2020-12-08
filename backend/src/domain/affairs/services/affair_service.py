from typing import Any, Dict, List, Union
from flask import current_app
from requests import Response

from adapters.http.sig import SigApiAdapter
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository


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
    def list_affairs_by_insee_and_postal_codes(insee_code: Union[str, List[str]],
                                               postal_code: Union[str, List[str]],
                                               repo: AbstractAffairRepository) -> List[Dict[str, Any]]:
        response: Response = SigApiAdapter.code_territory_search(insee_code=insee_code, postal_code=postal_code)
        result: dict = response.json()
        affairs: List[AffairEntity] = repo.get_from_city_codes(multipolygon=result["geometrie"]["coordinates"][0][0])
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
