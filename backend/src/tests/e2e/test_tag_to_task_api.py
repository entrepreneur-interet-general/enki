from typing import Dict
from uuid import uuid4

from flask.testing import FlaskClient

from domain.tasks.ports.task_repository import AlreadyExistingTagInThisTask
from .test_tag_api import BASE_PATH_TAG
from .test_task_api import BASE_PATH_TASK, get_task
from ..factories.tag import tag_factory
from ..factories.task import task_factory
from ..helpers.filter import filter_dict_with_keys

def test_add_task_add_tag_then_link_them(app, client: FlaskClient):
    app.context.reset()
    task1 = task_factory()
    _ = post_add_task(client, task1)
    tag1 = tag_factory()
    _ = post_add_tag(client, tag1)

    # fetching added task
    link_task1_tag1_response = post_add_tag_to_task(client, task1["uuid"], tag1["uuid"])
    assert link_task1_tag1_response.status_code == 201
    assert link_task1_tag1_response.json == {
        "message": f"tag {tag1['uuid']} successfully added from task {task1['uuid']}"}

    link_task1_tag1_response = post_add_tag_to_task(client, task1["uuid"], tag1["uuid"])
    assert link_task1_tag1_response.status_code == AlreadyExistingTagInThisTask.code
    assert link_task1_tag1_response.json == {
        "message": AlreadyExistingTagInThisTask.description
    }

    task1_get_response = get_task(client, task1["uuid"])
    assert task1_get_response.status_code == 200
    task_tags = task1_get_response.json["task"]["tags"]
    assert filter_dict_with_keys(task_tags[0], tag1) == tag1


def test_add_task_add_tag_then_link_them_and_unlinks(app, client: FlaskClient):
    app.context.reset()
    task1 = task_factory()
    _ = post_add_task(client, task1)
    tag1 = tag_factory()
    _ = post_add_tag(client, tag1)

    post_add_tag_to_task(client, task1["uuid"], tag1["uuid"])
    unlink_task1_tag1_response = post_delete_tag_to_task(client, task1["uuid"], tag1["uuid"])
    assert unlink_task1_tag1_response.status_code == 202
    assert unlink_task1_tag1_response.json == {
        "message": f"tag {tag1['uuid']} successfully deleted from task {task1['uuid']}"}

    task1_get_response = get_task(client, task1["uuid"])
    assert task1_get_response.status_code == 200
    task_tags = task1_get_response.json["task"]["tags"]
    assert len(task_tags) == 0


def post_add_task(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TASK, json=body)


def post_add_tag(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TAG, json=body)


def post_add_tag_to_task(client: FlaskClient, task_uuid: str, tag_uuid: str):
    return client.put(BASE_PATH_TASK + f"/{task_uuid}/tags/{tag_uuid}")


def post_delete_tag_to_task(client: FlaskClient, task_uuid: str, tag_uuid: str):
    return client.delete(BASE_PATH_TASK + f"/{task_uuid}/tags/{tag_uuid}")
