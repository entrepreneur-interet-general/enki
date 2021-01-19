from typing import Any, Dict, List
from domain.phonebook.entities.contact import ContactEntity
from domain.messages.schemas.schema import ContactSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class ContactService:
    schema = ContactSchema

    @staticmethod
    def add_contact(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        contact: ContactEntity = ContactService.schema().load(data)
        return_value = ContactService.schema().dump(contact)

        with uow:
            uow.contact.add(contact)
        return return_value

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
