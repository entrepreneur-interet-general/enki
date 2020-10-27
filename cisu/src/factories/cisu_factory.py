from .alert_factory import PrimaryAlertFactory
from .commons import AddressTypeFactory, RecipientsFactory
from .factory import Factory
from .location_factory import LocationTypeFactory
from .uid_factory import UidFactory
from ..entities.cisu_entity import CisuEntity, MessageCisuEntity, MessageType, Status, CreateEvent
from ..entities.commons import DateType, Severity


class CreateEventFactory(Factory):
    def build(self) -> CreateEvent:
        return CreateEvent(
            eventId=UidFactory().build(),
            createdAt=DateType(self.clock_seed.generate()),
            severity=Severity.random(),
            eventLocation=LocationTypeFactory().build(),
            primaryAlert=PrimaryAlertFactory().build(),
            otherAlert=[],
        )


class MessageCisuFactory(Factory):
    def build(self) -> MessageCisuEntity:
        return MessageCisuEntity(
            messageId=UidFactory().build(),
            sender=AddressTypeFactory().build(),
            sentAt=DateType(self.clock_seed.generate()),
            msgType=MessageType.random(),
            status=Status.random(),
            recipients=RecipientsFactory().build(),
            choice=CreateEventFactory().build()
        )


class CisuEntityFactory(Factory):
    def build(self) -> CisuEntity:
        return CisuEntity(
            message=MessageCisuFactory().build()
        )
