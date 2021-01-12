from typing import Dict
from uuid import uuid4

from flask.testing import FlaskClient

from domain.messages.ports.message_repository import AlreadyExistingMessageUuid, NotFoundMessage
from entrypoints.flask_app import app
from ..factories.message import message_factory
from ..helpers.filter import filter_dict_with_keys

BASE_PATH_TASK: str = "/api/enki/v1/messages"


def test_add_message_then_recovers_it_and_recovers_all(app, client: FlaskClient):
    message1 = message_factory()
    add_message_response = post_add_message(client, message1)

    assert add_message_response.status_code == 201
    assert add_message_response.json['message'] == "success"

    # fetching added message
    fetched_message1_response = get_message(client, message_uuid=message1["uuid"])
    assert fetched_message1_response.status_code == 200
    assert filter_dict_with_keys(fetched_message1_response.json["data"], message1) == message1

    # adding extra message
    message2 = message_factory()
    post_add_message(client, message2)

    # fetching all messages
    fetched_all_messages_response = get_all_messages(client)
    assert fetched_all_messages_response.status_code == 200
    print(fetched_all_messages_response.json["data"])
    print(message1)
    print(message2)
    filtered_list = ([filter_dict_with_keys(message, message1) for message in fetched_all_messages_response.json["data"]])
    assert filtered_list == [message1, message2] or filtered_list == [message2, message1]


def test_already_exists_message(app, client: FlaskClient):
    message1 = message_factory()

    post_add_message(client, message1)

    add_already_exists_message_response = post_add_message(client, message1)
    assert add_already_exists_message_response.status_code == AlreadyExistingMessageUuid.code
    assert add_already_exists_message_response.json == {"message": AlreadyExistingMessageUuid.description}


def test_not_found_exists_message(app, client: FlaskClient):
    message1 = message_factory()

    post_add_message(client, message1)

    fetch_random_message_response = get_message(client, str(uuid4()))
    assert fetch_random_message_response.status_code == NotFoundMessage.code
    assert fetch_random_message_response.json == {"message": NotFoundMessage.description}


def post_add_message(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TASK, json=body)


def get_message(client: FlaskClient, message_uuid: str):
    return client.get(BASE_PATH_TASK + f"/{message_uuid}")


def get_all_messages(client: FlaskClient):
    return client.get(BASE_PATH_TASK)
