from typing import Any, Dict, List, Union

from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.ports.message_repository import AlreadyExistingTagInThisMessage, \
    AlreadyExistingResourceInThisMessage
from domain.evenements.schemas import MessageSchema, TagSchema
from domain.evenements.schemas.resource_schema import ResourceSchema
from domain.users.entities.user import UserEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class MessageService:
    schema = MessageSchema

    @staticmethod
    def add_message(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        tag_ids = data.pop("tags", [])
        resource_ids = data.pop("resources", [])
        creator_id = data.pop("creator_id")

        with uow:
            message: MessageEntity = MessageService.schema().load(data)
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=message.evenement_id)
            message.assign_evenement(evenement=evenement)
            user: UserEntity = uow.user.get_by_uuid(uuid=creator_id)
            uow.message.add(message)
            message.set_creator(user=user)
            MessageService.add_tags(message=message, tag_ids=tag_ids, uow=uow)
            MessageService.add_resources(message=message, resource_ids=resource_ids, uow=uow)
            new_message = uow.message.get_by_uuid(message.uuid)
            return MessageService.schema().dump(new_message)

    @staticmethod
    def add_tags(message: MessageEntity, tag_ids: List[str], uow: AbstractUnitOfWork):
        if tag_ids:
            tags = uow.tag.get_by_uuid_list(tag_ids)
            for tag in tags:
                message.add_tag(tag=tag)

    @staticmethod
    def add_resources(message: MessageEntity, resource_ids: List[str], uow: AbstractUnitOfWork):
        if resource_ids:
            resources = uow.resource.get_by_uuid_list(resource_ids)
            for resource in resources:
                message.add_resource(resource=resource)

    @staticmethod
    def add_tag_to_message(message_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            results = message.get_tag_by_id(uuid=tag_uuid)
            if results:
                raise AlreadyExistingTagInThisMessage()
            tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
            message.add_tag(tag=tag)

    @staticmethod
    def remove_tag_to_message(message_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            tag: TagEntity = message.get_tag_by_id(uuid=tag_uuid)
            message.remove_tag(tag=tag)

    @staticmethod
    def add_resource_to_message(message_uuid, resource_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            results = message.get_resource_by_id(uuid=resource_uuid)
            if results:
                raise AlreadyExistingResourceInThisMessage()
            resource: ResourceEntity = uow.resource.get_by_uuid(uuid=resource_uuid)
            message.add_resource(resource=resource)

    @staticmethod
    def remove_resource_to_message(message_uuid, resource_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            resource: ResourceEntity = message.get_resource_by_id(uuid=resource_uuid)
            message.remove_resource(resource=resource)

    @staticmethod
    def list_tags(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(uuid=uuid)
            return TagSchema(many=True).dump(message.get_tags())

    @staticmethod
    def list_resources(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(uuid=uuid)
            return ResourceSchema(many=True).dump(message.get_resources())

    @staticmethod
    def get_message_resource(uuid: str, resource_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(uuid=uuid)
            resource: ResourceEntity = message.get_resource_by_id(uuid=resource_uuid)
            return ResourceSchema().dump(resource)

    @staticmethod
    def get_message_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(uuid=uuid)
            tag: TagEntity = message.get_tag_by_id(uuid=tag_uuid)
            return TagSchema().dump(tag)

    @staticmethod
    def list_messages(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            messages: List[MessageEntity] = uow.message.get_all()
            return MessageService.schema(many=True).dump(messages)

    @staticmethod
    def list_messages_by_query(evenement_id: str, tag_ids: Union[str, List[str], None], uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        if isinstance(tag_ids, str):
            tag_ids = [tag_ids]
        with uow:
            messages: List[MessageEntity] = uow.message.get_messages_by_query(evenement_id=evenement_id, tag_ids=tag_ids)
            return MessageService.schema(many=True).dump(messages)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            message = uow.message.get_by_uuid(uuid)
            return MessageService.schema().dump(message)
