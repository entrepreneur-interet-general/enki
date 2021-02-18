from typing import List, Union

from flask import current_app
from sqlalchemy.orm import Session

from domain.messages.entities.resource import ResourceEntity
from domain.messages.ports.message_repository import AbstractMessageRepository, AlreadyExistingMessageUuid, NotFoundMessage, MessagesList
from domain.messages.entities.message_entity import MessageEntity
from domain.messages.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin


class PgMessageRepository(PgRepositoryMixin, AbstractMessageRepository):


    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=MessageEntity)
        AbstractMessageRepository.__init__(self)

    def add_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        message.tags.append(tag)

    def remove_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        message.tags.remove(tag)

    def add_resource_to_message(self, message: MessageEntity,  resource: ResourceEntity) -> None:
        message.resources.append(resource)
        resource.message_id = message.uuid

    def remove_resource_to_message(self, message: MessageEntity, resource: ResourceEntity) -> None:
        message.resources.remove(resource)
        resource.message_id = None

    def _match_uuid(self, uuid: str) -> MessageEntity:
        matches = self.session.query(MessageEntity).filter(MessageEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, message: MessageEntity) -> None:
        if self._match_uuid(message.uuid):
            raise AlreadyExistingMessageUuid()
        self.session.add(message)

    def get_all(self) -> List[MessageEntity]:
        return self.session.query(self.entity_type).order_by(self.entity_type.created_at.desc()).all()

    def _get_tag_by_message(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        match = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in match.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]

    def _get_resource_by_message(self, uuid: str, resource_uuid: str) -> Union[ResourceEntity, None]:
        match = self.get_by_uuid(uuid=uuid)
        matches = [resource for resource in match.resources if resource.uuid == resource_uuid]
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> MessagesList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def get_messages_by_query(self, evenement_id: str, tag_ids: List[str]) -> MessagesList:
        query = self.session.query(self.entity_type)
        if evenement_id:
            query = query.filter(self.entity_type.evenement_id == evenement_id)
        if tag_ids:
            current_app.logger.info(f"tag_ids {tag_ids}")
            query = query.join(TagEntity, self.entity_type.tags).filter(TagEntity.uuid.in_(tag_ids))

        matches = query.all()
        return matches