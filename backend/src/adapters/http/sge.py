import requests
from cisu.entities.cisu_entity import AddressType
from cisu.entities.commons.common_alerts import AnyURI
from cisu.entities.edxl_entity import EdxlEntity
from cisu.factories.edxl_factory import EdxlMessageFactory
from flask import current_app
from requests import Response

from domain.core import events
from entrypoints.config import EnkiConfig


class SgeHelper:
    base_url: str = EnkiConfig.SGE_HUB_BASE_URI

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
        edxl_message: EdxlEntity = event.data
        ack_message = EdxlMessageFactory.build_ack_from_another_message(
            sender_address=AddressType(current_app.config['ENKI_SGE_ID'],
                                       AnyURI(current_app.config['ENKI_SGE_ADDRESS'])),
            other_message=edxl_message,
        )

        return SgeHelper.send_ack_message(ack_message.to_xml())
