from typing import Any, Dict, List
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.info_entity import InformationEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class InformationService:
    @staticmethod
    def add_information(uuid: str, title: str, description: str, uow: AbstractUnitOfWork):
        new_information = InformationEntity(uuid=uuid, title=title, description=description)
        with uow:
            uow.information.add(new_information)

    @staticmethod
    def add_tag_to_information(information_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            uow.information.add_tag_to_information(information_uuid, tag_uuid)

    @staticmethod
    def remove_tag_to_information(information_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            uow.information.remove_tag_to_information(information_uuid, tag_uuid)

    @staticmethod
    def list_tags(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            information: InformationEntity = uow.information.get_tags(uuid)
            return [tag.to_dict() for tag in information.tags]

    @staticmethod
    def get_information_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag: TagEntity = uow.information.get_tag_by_information(uuid=uuid, tag_uuid=tag_uuid)
            return tag.to_dict()

    @staticmethod
    def list_informations(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            informations: List[InformationEntity] = uow.information.get_all()
            serialized_informations = [information.to_dict() for information in informations]
            return serialized_informations

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            information = uow.information.get_by_uuid(uuid)
            return information.to_dict()
