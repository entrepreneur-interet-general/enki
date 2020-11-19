from dataclasses import dataclass
from dataclasses_json import dataclass_json
from domain.affairs.cisu.entities.cisu_entity import CreateEvent


@dataclass_json
@dataclass
class AffairEntity(CreateEvent):
    """

    """

    @property
    def uuid(self):
        return self.eventId

    @classmethod
    def from_create_event(cls, create_event: CreateEvent):
        return cls(
            eventId=create_event.eventId,
            createdAt=create_event.createdAt,
            severity=create_event.severity,
            eventLocation=create_event.eventLocation,
            primaryAlert=create_event.primaryAlert,
            otherAlert=create_event.otherAlert
        )
