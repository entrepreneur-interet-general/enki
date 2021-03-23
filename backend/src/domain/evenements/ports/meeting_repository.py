import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.evenements.entities.meeting_entity import MeetingEntity

MeetingsList = List[MeetingEntity]


class AlreadyExistingMeetingUuid(HTTPException):
    code = 409
    description = "Meeting already exists"


class NotFoundMeeting(HTTPException):
    code = 404
    description = "Meeting not found"


class AbstractMeetingRepository(abc.ABC):
    def add(self, meeting: MeetingEntity) -> None:
        if self._match_uuid(meeting.uuid):
            raise AlreadyExistingMeetingUuid()
        self._add(meeting)

    def get_by_uuid(self, uuid: str) -> MeetingEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundMeeting
        return matches

    @abc.abstractmethod
    def get_all(self) -> MeetingsList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, meeting: MeetingEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[MeetingEntity, None]:
        raise NotImplementedError