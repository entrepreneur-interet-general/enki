from typing import Any, Dict, List, Union
from uuid import uuid4

from requests import Response
from cisu.entities.edxl_entity import EdxlEntity
import xml.dom.minidom

from adapters.http.sig import SigApiAdapter
from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.affairs.ports.simple_affair_repository import ThisAffairNotAssignToThisEvent
from domain.evenements.entity import EvenementEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class AffairService:
    @staticmethod
    def add_affair(affair: AffairEntity, uow: AbstractUnitOfWork):
        with uow:
            uow.affair.add(affair)
            simple_affair = SimpleAffairEntity(
                uuid=str(uuid4()),
                evenement_id=None,
                sge_hub_id=affair.uuid,
            )
            uow.simple_affair.add(simple_affair)
            return affair

    @staticmethod
    def add_affair_from_xml(xml_string: str, uow: AbstractUnitOfWork) -> AffairEntity:
        affair: AffairEntity = AffairService.build_affair_from_xml_string(xml_string=xml_string)
        AffairService.add_affair(affair=affair, uow=uow)

    @staticmethod
    def assign_affair_to_evenement(affair_id: str, evenement_id: str, uow: AbstractUnitOfWork):
        with uow:
            affair: SimpleAffairEntity = uow.simple_affair.get_by_uuid(uuid=affair_id)
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_id)
            uow.simple_affair.assign_evenement_to_affair(affair, evenement)

    @staticmethod
    def delete_affair_to_evenement(affair_id: str, evenement_id: str, uow: AbstractUnitOfWork):
        with uow:
            affair: SimpleAffairEntity = uow.simple_affair.get_by_uuid(uuid=affair_id)
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_id)
            if affair.evenement_id == evenement.uuid:
                uow.simple_affair.delete_affair_from_evenement(affair)
            else:
                raise ThisAffairNotAssignToThisEvent

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork):
        with uow:
            return uow.affair.get_by_uuid(uuid=uuid).to_dict()

    @staticmethod
    def list_affairs(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            affairs: List[AffairEntity] = uow.affair.get_all()
            serialized_affairs = [affair.to_dict() for affair in affairs]
            return serialized_affairs

    @staticmethod
    def list_affairs_by_insee_and_postal_codes(insee_code: Union[str, List[str], None],
                                               postal_code: Union[str, List[str], None],
                                               uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            response: Response = SigApiAdapter.code_territory_search(insee_code=insee_code, postal_code=postal_code)
            result: dict = response.json()
            if result["geometrie"]:
                affairs: List[AffairEntity] = uow.affair.get_from_polygon(
                    multipolygon=result["geometrie"]["coordinates"][0][0])
                serialized_affairs = [affair.to_dict() for affair in affairs]
                return serialized_affairs
            return []

    @staticmethod
    def get_random_affair(uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            affair: AffairEntity = uow.affair.get_one()
            return affair.to_dict()

    @staticmethod
    def get_random_list_affairs(uow: AbstractUnitOfWork, n=10) -> List[Dict[str, Any]]:
        with uow:
            affairs: List[AffairEntity] = uow.affair.get_many(n)
            return [affair.to_dict() for affair in affairs]

    @staticmethod
    def build_affair_from_xml_string(xml_string: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parseString(xml_string)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())

    @staticmethod
    def build_affair_from_xml_file(xml_path: str) -> AffairEntity:
        affair_dom = xml.dom.minidom.parse(xml_path)
        edxl_message = EdxlEntity.from_xml(affair_dom)
        return AffairEntity(**edxl_message.resource.message.choice.to_dict())
