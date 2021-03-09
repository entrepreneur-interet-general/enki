import random

from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.schemas import MessageSchema


def build_message_data():
    return {
        "title": f"title-{random.randint(1, 100)}",
        "description": f"description-{random.randint(1, 100)}",
        "evenement_id": f"evenement-{random.randint(1, 100)}",
        "type": "info",
    }


def test_message_load():
    message_data = build_message_data()
    message: MessageEntity = MessageSchema().load(message_data)
    assert isinstance(message, MessageEntity)
    assert message.title == message_data["title"]

