from typing import Any, Dict, List

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.info_entity import InformationEntity
from domain.tasks.ports.information_repository import AlreadyExistingTagInThisInformation, NotFoundTagInThisInformation
from domain.tasks.schema import InformationSchema, TagSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class InformationService:
    schema = InformationSchema

    @staticmethod
    def add_information(data: Dict[str, Any], uow: AbstractUnitOfWork):
        tags = data.pop("tags", [])
        information: InformationEntity = InformationService.schema().load(data)
        with uow:
            uow.information.add(information)
            if tags:
                tags = uow.tag.get_by_uuid_list(tags)
                for tag in tags:
                    uow.information.add_tag_to_information(information=information, tag=tag)
            new_task = uow.information.get_by_uuid(information.uuid)
            return InformationService.schema().dump(new_task)

    @staticmethod
    def add_tag_to_information(information_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            match: InformationEntity = uow.information.get_by_uuid(information_uuid)
            results = uow.information.get_tag_by_information(uuid=information_uuid, tag_uuid=tag_uuid)
            if results:
                raise AlreadyExistingTagInThisInformation()
            tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
            uow.information.add_tag_to_information(information=match, tag=tag)

    @staticmethod
    def remove_tag_to_information(information_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            if not uow.information.get_tag_by_information(uuid=information_uuid, tag_uuid=tag_uuid):
                raise NotFoundTagInThisInformation()
            match: InformationEntity = uow.information.get_by_uuid(information_uuid)
            tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
            uow.information.remove_tag_to_information(match, tag=tag)

    @staticmethod
    def list_tags(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            information: InformationEntity = uow.information.get_tags(uuid)
            return TagSchema(many=True).dump(information.tags)

    @staticmethod
    def get_information_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag: TagEntity = uow.information.get_tag_by_information(uuid=uuid, tag_uuid=tag_uuid)
            return TagSchema().dump(tag)

    @staticmethod
    def list_informations(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            informations: List[InformationEntity] = uow.information.get_all()
            return InformationService.schema(many=True).dump(informations)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            information = uow.information.get_by_uuid(uuid)
            return InformationService.schema().dump(information)
