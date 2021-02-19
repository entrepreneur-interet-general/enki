from domain.messages.entities.message_entity import MessageEntity
from service_layer.unit_of_work import AbstractUnitOfWork
from uuid import uuid4
import pytest

def build_event(uow: AbstractUnitOfWork):
    pass



def test_add_message(uow: AbstractUnitOfWork):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    expected_event = "event_id"
    message = MessageEntity(uuid,
                            title=expected_title,
                            description=expected_description,
                            evenement_id=expected_event
                            )
    with uow:
        uow.message.add(message)

        assert uow.message.get_all()[0] == message


def test_fails_to_add_message_when_already_exists(uow: AbstractUnitOfWork):
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
                             evenement_id=serialized_message1["evenement_id"])
    with uow:
        uow.message.add(message1)

        with pytest.raises(AlreadyExistingMessageUuid):
            uow.message.add(message1)


def test_list_messages(uow: AbstractUnitOfWork):
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

    with uow:
        uow.message.add(message1)

        messages = uow.message.get_all()

        assert len(messages) == 1
        assert messages[0] == message1


def test_get_by_uuid_when_not_present(uow: AbstractUnitOfWork):
    with uow:
        with pytest.raises(NotFoundMessage):
            uow.message.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_message_present(uow: AbstractUnitOfWork):
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
    with uow:
        uow.message.add(message1)

        message = uow.message.get_by_uuid(message1_uuid)
        assert message == message1
