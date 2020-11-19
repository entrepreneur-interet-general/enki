from datetime import datetime, timedelta
from uuid import uuid4

from typing import List

from .cisu_factory import CisuEntityFactory, MessageCisuFactory
from .factory import Factory
from .uid_factory import UidFactory
from ..entities.edxl_entity import EdxlEntity
from ..entities.cisu_entity import CisuEntity, MessageType, Status, AddressType, Recipients, AckMessage
from ..entities.commons import DateType


class EdxlMessageFactory(Factory):
    def build(self) -> EdxlEntity:
        return self.create(
            uuid=UidFactory().build(),
            sender_id=UidFactory().build(),
            date_time_sent=self.clock_seed.generate(),
            date_time_expires=self.clock_seed.generate(),
            distribution_status="status",
            distribution_kind="kind",
            resource=CisuEntityFactory().build(),
            receivers_address=["sgc-enki"]
        )

    @staticmethod
    def create(uuid: str,
               sender_id: str,
               date_time_sent: DateType,
               date_time_expires: DateType,
               distribution_status: str,
               distribution_kind: str,
               receivers_address: List[str],
               resource: CisuEntity) -> EdxlEntity:
        return EdxlEntity(
            distributionID=uuid,
            senderID=sender_id,
            dateTimeSent=date_time_sent,
            dateTimeExpires=date_time_expires,
            distributionStatus=distribution_status,
            distributionKind=distribution_kind,
            resource=resource,
            receiversAddress=receivers_address
        )

    @classmethod
    def build_ack_from_another_message(cls,
                                       sender_address: AddressType,
                                       recipients,
                                       messageId: str,
                                       other_message: EdxlEntity) -> EdxlEntity:
        return cls.create(
            uuid=str(uuid4()),
            date_time_sent=DateType(datetime.now()),
            date_time_expires=DateType(datetime.now() + timedelta(days=1)),
            distribution_status="Actual",
            distribution_kind="Ack",
            sender_id=sender_address.URI.path_name,
            receivers_address=[other_message.resource.message.sender.URI.path_name],
            resource=CisuEntity(
                message=MessageCisuFactory.create(
                    uuid=str(uuid4()),
                    sender=sender_address,
                    sent_at=DateType(datetime.now()),
                    msg_type=MessageType.ACK,
                    status=Status.SYSTEM,
                    recipients=Recipients([other_message.resource.message.sender]),
                    choice=AckMessage(ackMessageId=messageId)
                )
            )

        )
