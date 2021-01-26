from uuid import uuid4
import requests
from flask import current_app
from requests import Response

from cisu.entities.edxl_entity import EdxlEntity
from cisu.entities.cisu_entity import AddressType
from cisu.entities.commons.common_alerts import AnyURI
from cisu.factories.edxl_factory import EdxlMessageFactory
from entrypoints.config import EnkiConfig
from domain.core import events


class SgeHelper:
    base_url: str = EnkiConfig.KEYCLOAK_BASE_URL
    realm: str = EnkiConfig.KEYCLOAK_REALM

    def __init__(self):
        self.KEYCLOAK_USERS_ENDPOINT = f"{self.base_url}/admin/realms/{self.realm}/users"

    KEYCLOAK_GROUPS_ENDPOINT = `${KEYCLOAK_URL} / admin / realms /${KEYCLOAK_REALM} / groups
    `;

    @staticmethod
    def update_user(xml_ack_message: str) -> requests.Response:
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
