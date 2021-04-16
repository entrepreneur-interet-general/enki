from typing import Any, Dict, List, Union

from flask import current_app

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.entities.meeting_entity import MeetingEntity
from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.entities.resource import ResourceEntity
from domain.evenements.entities.tag_entity import TagEntity
from domain.evenements.ports.message_repository import AlreadyExistingTagInThisMessage, \
    AlreadyExistingResourceInThisMessage
from domain.evenements.schemas.message_tag_schema import MessageSchema, TagSchema
from domain.evenements.schemas.resource_schema import ResourceSchema
from domain.users.entities.user import UserEntity
from entrypoints.extensions import event_bus
from service_layer.unit_of_work import AbstractUnitOfWork
from werkzeug.exceptions import HTTPException


class NotAuthorizedOnThisMessage(HTTPException):
    code = 401
    description = "Action interdite sur ce message"

class MessageService:
    schema = MessageSchema

    @staticmethod
    def save_message(message: MessageEntity, uow: AbstractUnitOfWork):
        uow.message.add(message)

    @staticmethod
    def add_message(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        tag_ids = data.pop("tags", [])
        resource_ids = data.pop("resources", [])
        creator_id = data.pop("creator_id")
        evenement_id = data.pop("evenement_id")

        with uow:
            message: MessageEntity = MessageService.schema().load(data)
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement_id)
            MessageService.save_message(message, uow=uow)
            evenement.add_message(message=message)
            user: UserEntity = uow.user.get_by_uuid(uuid=creator_id)
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
    def add_tag_to_message(message_uuid: str, tag_uuid: str, user_uuid:str,  uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            if message.is_authorized_to_modify(user_uuid):
                results = message.get_tag_by_id( uuid=tag_uuid)
                if results:
                    raise AlreadyExistingTagInThisMessage()
                tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
                message.add_tag(tag=tag)
            else:
                raise NotAuthorizedOnThisMessage()


    @staticmethod
    def remove_tag_to_message(message_uuid: str, tag_uuid: str, user_uuid:str, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            if message.is_authorized_to_modify(user_uuid):
                tag: TagEntity = message.get_tag_by_id(uuid=tag_uuid)
                message.remove_tag(tag=tag)
            else:
                raise NotAuthorizedOnThisMessage()

    @staticmethod
    def add_resource_to_message(message_uuid:str, resource_uuid:str,  user_id:str, uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            if message.is_authorized_to_modify(user_id):
                results = message.get_resource_by_id(uuid=resource_uuid)
                if results:
                    raise AlreadyExistingResourceInThisMessage()
                resource: ResourceEntity = uow.resource.get_by_uuid(uuid=resource_uuid)
                message.add_resource(resource=resource)
            else:
                raise NotAuthorizedOnThisMessage()

    @staticmethod
    def remove_resource_to_message(message_uuid:str, resource_uuid:str,user_id:str,  uow: AbstractUnitOfWork) -> None:
        with uow:
            message: MessageEntity = uow.message.get_by_uuid(message_uuid)
            if message.is_authorized_to_modify(user_id):
                resource: ResourceEntity = message.get_resource_by_id(uuid=resource_uuid)
                message.remove_resource(resource=resource)
            else:
                raise NotAuthorizedOnThisMessage()

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
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            message = uow.message.get_by_uuid(uuid)
            return MessageService.schema().dump(message)

    @staticmethod
    def add_message_from_meeting(meeting: MeetingEntity, uow: AbstractUnitOfWork):
        current_app.logger.info(f"UOW type {type(uow)}")
        with uow:
            message: MessageEntity = MessageEntity.from_meeting(meeting=meeting)
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=meeting.evenement_id)
            MessageService.save_message(message, uow=uow)
            evenement.add_message(message=message)
            user: UserEntity = uow.user.get_by_uuid(uuid=meeting.creator_id)
            message.set_creator(user=user)

    @staticmethod
    def add_message_from_affair(affair: SimpleAffairEntity, evenement: EvenementEntity, uow: AbstractUnitOfWork):
        message: MessageEntity = MessageEntity.from_affair(affair=affair)
        MessageService.save_message(message, uow=uow)
        evenement.add_message(message=message)
