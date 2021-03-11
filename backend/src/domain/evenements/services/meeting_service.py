from typing import Any, Dict, List

from domain.evenements.entities.meeting_entity import MeetingEntity
from domain.evenements.schemas.meeting_schema import MeetingSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class MeetingService:
    schema = MeetingSchema

    @staticmethod
    def add_meeting(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        meeting: MeetingEntity = MeetingService.schema().load(data)
        with uow:
            uow.meeting.add(meeting)
            return MeetingService.schema().dump(uow.meeting.get_by_uuid(meeting.uuid))

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            meeting = uow.meeting.get_by_uuid(uuid)
            return MeetingService.schema().dump(meeting)
