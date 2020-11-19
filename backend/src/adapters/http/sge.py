from uuid import uuid4
import requests
from flask import current_app
from requests import Response

from domain.affairs.cisu import EdxlEntity
from domain.affairs.cisu.entities.cisu_entity import AddressType
from domain.affairs.cisu.entities.commons.common_alerts import AnyURI
from domain.affairs.cisu.factories.edxl_factory import EdxlMessageFactory
from domain.affairs.entities.affair_entity import AffairEntity
from entrypoints.config import SapeursConfig
from domain.core import events


class SgeHelper:
    base_url: str = SapeursConfig.SGE_HUB_BASE_URI

    @staticmethod
    def send_ack_message(xml_ack_message: str) -> requests.Response:
        response = requests.post(SgeHelper.base_url + "/messages",
                                 data=xml_ack_message,
                                 headers={
                                     'Content-Type': "text/xml",
                                 })

        return response

    @staticmethod
    def send_ack_to_sge(event: events.AffairCreatedEvent) -> Response:
        edxl_message: AffairEntity = event.data
        ack_message = EdxlMessageFactory.build_ack_from_another_message(
            sender_address=AddressType(current_app.config['ENKI_SGE_ID'],
                                       AnyURI(current_app.config['ENKI_SGE_ADDRESS'])),
            other_message=edxl_message,
        )

        return SgeHelper.send_ack_message(ack_message.to_xml())
