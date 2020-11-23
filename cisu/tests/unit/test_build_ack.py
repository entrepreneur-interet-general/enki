import pathlib
from datetime import datetime
from datetime import timedelta
from uuid import uuid4

import pytest
import xmlschema

from cisu.src import EdxlEntity
from cisu.src.entities.cisu_entity import CisuEntity, AddressType, MessageType, Status, AckMessage, \
    Recipients
from cisu.src.entities.cisu_entity import Recipient
from cisu.src.entities.commons import DateType
from cisu.src.entities.commons.common_alerts import AnyURI
from cisu.src.factories.cisu_factory import MessageCisuFactory
from cisu.src.factories.edxl_factory import EdxlMessageFactory
import xml.dom.minidom
from tempfile import NamedTemporaryFile


def test_build_ack_message():
    ack_message_id = str(uuid4())
    edxl: EdxlEntity = EdxlMessageFactory.create(
        uuid=str(uuid4()),
        date_time_sent=DateType(datetime.now()),
        date_time_expires=DateType(datetime.now() + timedelta(days=1)),
        distribution_status="Actual",
        distribution_kind="Report",
        sender_id=str(uuid4()),
        receivers_address=["sgc-enki"],
        resource=CisuEntity(
            message=MessageCisuFactory.create(
                uuid=str(uuid4()),
                sender=AddressType("sgc-enki", AnyURI("uri")),
                sent_at=DateType(datetime.now()),
                msg_type=MessageType.ACK,
                status=Status.SYSTEM,
                recipients=Recipients([
                    Recipient("sgc-enki", AnyURI("uri"))
                ]),
                choice=AckMessage(ackMessageId=ack_message_id)
            )
        )
    )

    assert isinstance(edxl.resource.message.choice, AckMessage)
    assert edxl.resource.message.choice.ackMessageId == ack_message_id


filenames = list(pathlib.Path(pathlib.Path(__file__).parent.absolute()).glob("data/*.xml"))


@pytest.mark.parametrize("filename", filenames)
def test_build_ack_message_from_another_message(filename):
    dom = xml.dom.minidom.parse(str(filename))
    other_edxl = EdxlEntity.from_xml(dom)
    ack_sender = AddressType("test", AnyURI("test"))
    ack_message = EdxlMessageFactory.build_ack_from_another_message(
        sender_address=ack_sender,
        other_message=other_edxl,
    )

    assert isinstance(ack_message.resource.message.choice, AckMessage)
    assert ack_message.resource.message.choice.ackMessageId == other_edxl.resource.message.messageId
    assert ack_message.resource.message.recipients == Recipients([
        other_edxl.resource.message.sender
    ])
    assert ack_message.senderID == ack_sender.URI.path_name
    assert ack_message.resource.message.sender == ack_sender


@pytest.mark.parametrize("filename", filenames)
def test_edxl_xml_generation(filename):
    dom = xml.dom.minidom.parse(str(filename))
    other_edxl = EdxlEntity.from_xml(dom)

    ack_message = EdxlMessageFactory.build_ack_from_another_message(
        sender_address=AddressType("test", AnyURI("test")),
        other_message=other_edxl,
    )

    schema_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), "../../src/entities/schema/cisu.xsd")

    xml_string = ack_message.resource.message.to_xml()
    temp_file = NamedTemporaryFile(mode="w", suffix=".xml")
    with open(temp_file.name, "w") as f:
        f.write(xml_string)
    my_schema = xmlschema.XMLSchema(str(schema_path))
    print(my_schema.validate(temp_file.name))
    assert my_schema.is_valid(temp_file.name)
    temp_file.close()
