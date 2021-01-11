import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.messages.entities.tag_entity import TagEntity
from domain.messages.entities.message_entity import MessageEntity

MessagesList = List[MessageEntity]


class AlreadyExistingMessageUuid(HTTPException):
    code = 409
    description = "Message already exists"


class NotFoundMessage(HTTPException):
    code = 404
    description = "Message not found"


class AlreadyExistingTagInThisMessage(HTTPException):
    code = 409
    description = "Tag already exists in this message"


class NotFoundTagInThisMessage(HTTPException):
    code = 404
    description = "Tag not found in this message"


class AbstractMessageRepository(abc.ABC):

    def add(self, message: MessageEntity) -> None:
        if self._match_uuid(message.uuid):
            raise AlreadyExistingMessageUuid()
        self._add(message)

    def get_by_uuid(self, uuid: str) -> MessageEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundMessage
        return match

    def get_by_uuid_list(self, uuids: List[str]) -> MessagesList:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundMessage
        return matches

    def get_tag_by_message(self, uuid: str, tag_uuid: str) -> TagEntity:
        match = self._get_tag_by_message(uuid=uuid, tag_uuid=tag_uuid)
        if not match:
            raise NotFoundTagInThisMessage()
        return match

    def get_tags(self, uuid: str):
        match = self.get_by_uuid(uuid=uuid)
        if not match:
            raise NotFoundTagInThisMessage
        return match.tags

    @abc.abstractmethod
    def get_all(self) -> MessagesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, message: MessageEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[MessageEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> MessagesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tag_by_message(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        raise NotImplementedError


class InMemoryMessageRepository(AbstractMessageRepository):


    _messages: MessagesList = []

    def get_all(self) -> MessagesList:
        return self._messages

    def _match_uuid(self, uuid: str) -> Union[MessageEntity, None]:
        matches = [message for message in self._messages if message.uuid == uuid]
        if not matches:
            return None
        return matches[0]

    def _add(self, message: MessageEntity):
        self._messages.append(message)

    # next methods are only for test purposes
    @property
    def messages(self) -> MessagesList:
        return self._messages

    def set_messages(self, messages: MessagesList) -> None:
        self._messages = messages

    def add_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        message.tags.append(tag)

    def remove_tag_to_message(self, message: MessageEntity, tag: TagEntity) -> None:
        message.tags.remove(tag)

    def _get_tag_by_message(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        message: MessageEntity = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in message.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> MessagesList:
        matches = [message for message in self._messages if message.uuid in uuids]
        return matches
