from uuid import uuid4
import requests
from flask import current_app

from domain.affairs.cisu import EdxlEntity
from domain.affairs.cisu.entities.cisu_entity import AddressType
from domain.affairs.cisu.entities.commons.common_alerts import AnyURI
from domain.affairs.cisu.factories.edxl_factory import EdxlMessageFactory
from entrypoints.config import SapeursConfig
from domain.core import events


class SgeHelper:
    base_url: str = SapeursConfig.SGE_HUB_BASE_URI

    @staticmethod
    def send_ack_message(xml_ack_message: str) -> requests.Response:
        response = requests.post(SgeHelper.base_url,
                                 data=xml_ack_message,
                                 headers={
                                     'Content-Type': "text/xml",
                                 })

        return response

    @staticmethod
    def send_ack_to_sge(event: events.AffairCreatedEvent):
        edxl_message: EdxlEntity = event.data
        ack_message = EdxlMessageFactory.build_ack_from_another_message(
            my_uuid=str(uuid4()),
            my_sender_address=AddressType(SapeursConfig.ENKI_SGE_ID, AnyURI(SapeursConfig.ENKI_SGE_ADDRESS)),
            other_message=edxl_message,
        )

        SgeHelper.send_ack_message(ack_message.to_xml())
