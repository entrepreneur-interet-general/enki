from domain.evenements.entities.message_entity import MessageEntity
from domain.evenements.ports.message_repository import AlreadyExistingMessageUuid, NotFoundMessage, \
    AbstractMessageRepository
from uuid import uuid4
import pytest


def test_add_message(message_repo: AbstractMessageRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    expected_event = "event_id"
    message = MessageEntity(uuid,
                            title=expected_title,
                            description=expected_description,
                            evenement_id=expected_event
                            )
    message_repo.add(message)

    assert message_repo.get_all()[0] == message


def test_fails_to_add_message_when_already_exists(message_repo: AbstractMessageRepository):
    message1_uuid = str(uuid4())
    serialized_message1 = {
        "uuid": message1_uuid,
        "title": "Message 1 title",
        "description": "Message 1 description",
        "evenement_id": "event_id"
    }
    message1 = MessageEntity(uuid=message1_uuid,
                             title=serialized_message1["title"],
                             description=serialized_message1["description"],
                             evenement_id=serialized_message1["evenement_id"],
                             )
    message_repo.add(message1)

    with pytest.raises(AlreadyExistingMessageUuid):
        message_repo.add(message1)


def test_list_messages(message_repo: AbstractMessageRepository):
    message1_uuid = str(uuid4())
    serialized_message1 = {
        "uuid": message1_uuid,
        "title": "Message 1 title",
        "description": "Message 1 description",
        "evenement_id": "event_id"
    }
    message1 = MessageEntity(uuid=message1_uuid,
                             title=serialized_message1["title"],
                             description=serialized_message1["description"],
                             evenement_id=serialized_message1["evenement_id"],

                             )
    message_repo.add(message1)

    messages = message_repo.get_all()

    assert len(messages) == 1
    assert messages[0] == message1


def test_get_by_uuid_when_not_present(message_repo: AbstractMessageRepository):
    with pytest.raises(NotFoundMessage):
        message_repo.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_message_present(message_repo: AbstractMessageRepository):
    message1_uuid = str(uuid4())
    serialized_message1 = {
        "uuid": message1_uuid,
        "title": "Message 1 title",
        "description": "Message 1 description",
        "evenement_id": "event_id"

    }
    message1 = MessageEntity(uuid=message1_uuid,
                             title=serialized_message1["title"],
                             description=serialized_message1["description"],
                             evenement_id=serialized_message1["evenement_id"],

                             )
    message_repo.add(message1)

    message = message_repo.get_by_uuid(message1_uuid)
    assert message == message1
