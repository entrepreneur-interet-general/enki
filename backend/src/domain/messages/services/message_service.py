from typing import Any, Dict, List

from flask import current_app

from domain.messages.entities.tag_entity import TagEntity
from domain.messages.entities.message_entity import MessageEntity
from domain.messages.ports.message_repository import AlreadyExistingTagInThisMessage, NotFoundTagInThisMessage
from domain.messages.schema import MessageSchema, TagSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class MessageService:
    schema = MessageSchema

    @staticmethod
    def add_message(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        tags = data.pop("tags", [])
        message: MessageEntity = MessageService.schema().load(data)
        with uow:
            uow.message.add(message)
            if tags:
                tags = uow.tag.get_by_uuid_list(tags)
                for tag in tags:
                    uow.message.add_tag_to_message(message=message, tag=tag)
            new_message = uow.message.get_by_uuid(message.uuid)
            return MessageService.schema().dump(new_message)

    @staticmethod
    def add_tag_to_message(message_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            match: MessageEntity = uow.message.get_by_uuid(message_uuid)
            try:
                results = uow.message.get_tag_by_message(uuid=message_uuid, tag_uuid=tag_uuid)
                if results:
                    raise AlreadyExistingTagInThisMessage()
            except NotFoundTagInThisMessage:
                tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
                uow.message.add_tag_to_message(message=match, tag=tag)

    @staticmethod
    def remove_tag_to_message(message_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            if not uow.message.get_tag_by_message(uuid=message_uuid, tag_uuid=tag_uuid):
                raise NotFoundTagInThisMessage()
            match: MessageEntity = uow.message.get_by_uuid(message_uuid)
            tag: TagEntity = uow.tag.get_by_uuid(uuid=tag_uuid)
            uow.message.remove_tag_to_message(match, tag=tag)

    @staticmethod
    def list_tags(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            message: MessageEntity = uow.message.get_tags(uuid)
            return TagSchema(many=True).dump(message.tags)

    @staticmethod
    def get_message_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag: TagEntity = uow.message.get_tag_by_message(uuid=uuid, tag_uuid=tag_uuid)
            return TagSchema().dump(tag)

    @staticmethod
    def list_messages(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            messages: List[MessageEntity] = uow.message.get_all()
            return MessageService.schema(many=True).dump(messages)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            message = uow.message.get_by_uuid(uuid)
            return MessageService.schema().dump(message)
