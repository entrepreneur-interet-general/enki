from typing import List, Union

from sqlalchemy.orm import Session, lazyload

from domain.evenements.entities.meeting_entity import MeetingEntity
from domain.evenements.ports.meeting_repository import AbstractMeetingRepository, AlreadyExistingMeetingUuid
from .repository import PgRepositoryMixin

meetingsList = List[MeetingEntity]


class PgMeetingRepository(PgRepositoryMixin, AbstractMeetingRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=MeetingEntity)
        AbstractMeetingRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[MeetingEntity, None]:
        matches = self.session.query(MeetingEntity).options(lazyload('*')).filter(MeetingEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, meeting: MeetingEntity):
        if self._match_uuid(meeting.uuid):
            raise AlreadyExistingMeetingUuid()
        self.session.add(meeting)
        return meeting

    def get_all(self) -> meetingsList:
        return self.session.query(self.entity_type).all()
