from typing import Any, Dict

from domain.core.events import MeetingCreatedEvent
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.entities.meeting_entity import MeetingEntity
from domain.evenements.schemas.meeting_schema import MeetingSchema
from domain.users.entities.user import UserEntity
from entrypoints.extensions import event_bus
from service_layer.unit_of_work import AbstractUnitOfWork


class MeetingService:
    schema = MeetingSchema

    @staticmethod
    def add_meeting(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        meeting: MeetingEntity = MeetingService.schema().load(data)
        with uow:
            try:
                evenement: EvenementEntity = uow.evenement.get_by_uuid(meeting.evenement_id)
                meeting.evenement_id = evenement.uuid
                meeting.creator_id = data["creator_id"]
                uow.meeting.add(meeting)
                user: UserEntity = uow.user.get_by_uuid(uuid=data["creator_id"])
                meeting.set_creator(creator=user)
                uow.commit()
                return MeetingService.schema().dump(uow.meeting.get_by_uuid(meeting.uuid))
            finally:
                event_bus.publish(MeetingCreatedEvent(data=meeting), uow=uow)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return MeetingService.schema().dump(uow.meeting.get_by_uuid(uuid))

    @staticmethod
    def join_meeting(uuid: str, user_uuid: str, uow: AbstractUnitOfWork) -> str:
        with uow:
            meeting = uow.meeting.get_by_uuid(uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_uuid)
            meeting.add_participant(user=user)
            return meeting.link
