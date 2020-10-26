import abc
from typing import List, Union

from domain.affairs.entities.sge.sge_message_entity import SgeMessageEntity

sge_messagesList = List[SgeMessageEntity]


class AlreadyExistingSgeMessageUuid(Exception):
    pass


class NotFoundSgeMessage(Exception):
    pass


class AbstractSgeMessageRepository(abc.ABC):
    def get_by_uuid(self, uuid: str) -> SgeMessageEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundSgeMessage
        return matches[0]

    @abc.abstractmethod
    def get_all(self) -> sge_messagesList:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> List[SgeMessageEntity]:
        raise NotImplementedError


class InMemorySgeMessageRepository(AbstractSgeMessageRepository):
    _sge_messages: sge_messagesList = []

    def get_all(self) -> sge_messagesList:
        return self._sge_messages

    def _match_uuid(self, uuid: str) -> List[SgeMessageEntity]:
        return [sge_message for sge_message in self._sge_messages if sge_message.id == uuid]

    # next methods are only for test purposes
    @property
    def sge_messages(self) -> sge_messagesList:
        return self._sge_messages

    def set_sge_messages(self, sge_messages: sge_messagesList) -> None:
        self._sge_messages = sge_messages
