from typing import Dict
from flask.testing import FlaskClient

from domain.messages.ports.message_repository import AlreadyExistingTagInThisMessage
from .test_tag_api import BASE_PATH_TAG
from .test_message_api import BASE_PATH_TASK, get_message
from ..factories.tag import tag_factory
from ..factories.message import message_factory
from ..helpers.filter import filter_dict_with_keys


def test_add_message_add_tag_then_link_them(app, client: FlaskClient):
    message1 = message_factory()
    print("before the first add message")
    _ = post_add_message(client, message1)
    print("first add message")
    tag1 = tag_factory()
    _ = post_add_tag(client, tag1)

    # fetching added message
    link_message1_tag1_response = post_add_tag_to_message(client, message1["uuid"], tag1["uuid"])
    assert link_message1_tag1_response.status_code == 201
    assert link_message1_tag1_response.json == {
        "message": f"tag {tag1['uuid']} successfully added from message {message1['uuid']}"
    }

    link_message1_tag1_response = post_add_tag_to_message(client, message1["uuid"], tag1["uuid"])
    assert link_message1_tag1_response.status_code == AlreadyExistingTagInThisMessage.code
    assert link_message1_tag1_response.json == {
        "message": AlreadyExistingTagInThisMessage.description
    }

    message1_get_response = get_message(client, message1["uuid"])
    assert message1_get_response.status_code == 200
    message_tags = message1_get_response.json["data"]["tags"]
    assert filter_dict_with_keys(message_tags[0], tag1) == tag1


def test_add_message_add_tag_then_link_them_and_unlinks(app, client: FlaskClient):
    message1 = message_factory()
    _ = post_add_message(client, message1)
    tag1 = tag_factory()
    _ = post_add_tag(client, tag1)

    post_add_tag_to_message(client, message1["uuid"], tag1["uuid"])
    unlink_message1_tag1_response = post_delete_tag_to_message(client, message1["uuid"], tag1["uuid"])
    assert unlink_message1_tag1_response.status_code == 202
    assert unlink_message1_tag1_response.json == {
        "message": f"tag {tag1['uuid']} successfully deleted from message {message1['uuid']}"}

    message1_get_response = get_message(client, message1["uuid"])
    assert message1_get_response.status_code == 200
    message_tags = message1_get_response.json["data"]["tags"]
    assert len(message_tags) == 0


def post_add_message(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TASK, json=body)


def post_add_tag(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TAG, json=body)


def post_add_tag_to_message(client: FlaskClient, message_uuid: str, tag_uuid: str):
    return client.put(BASE_PATH_TASK + f"/{message_uuid}/tags/{tag_uuid}")


def post_delete_tag_to_message(client: FlaskClient, message_uuid: str, tag_uuid: str):
    return client.delete(BASE_PATH_TASK + f"/{message_uuid}/tags/{tag_uuid}")
