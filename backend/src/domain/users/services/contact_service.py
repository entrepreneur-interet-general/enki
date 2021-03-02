from typing import Any, Dict, List

from flask import current_app

from domain.users.entities.contact import ContactEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.contact import ContactSchema
from domain.users.services.user_service import UserService
from service_layer.unit_of_work import AbstractUnitOfWork


class ContactService:
    schema = ContactSchema

    @staticmethod
    def add_contact(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        contact: ContactEntity = ContactService.schema().load(data)
        uuid = contact.uuid
        with uow:
            uow.contact.add(contact)
            contact_position = UserService.build_position_from_group_id_ad_position_id(
                group_id=contact.group_id,
                position_id=contact.position_id,
                group_type=contact.group_type,
                uow=uow
            )
            contact.position = contact_position
        return ContactService.get_by_uuid(uuid, uow=uow)
    @staticmethod
    def get_contacts_from_query(query: str, uow: AbstractUnitOfWork):
        with uow:
            contacts: List[ContactEntity] = uow.contact.get_by_query(query=query)
            return ContactService.schema(many=True).dump(contacts)


    @staticmethod
    def list_contacts(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            contacts: List[ContactEntity] = uow.contact.get_all()
            return ContactService.schema(many=True).dump(contacts)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            contact = uow.contact.get_by_uuid(uuid)
            return ContactService.schema().dump(contact)

    @staticmethod
    def add_contact_from_user(user: UserEntity, uow: AbstractUnitOfWork):
        raise NotImplementedError  # TODO: Make it work
