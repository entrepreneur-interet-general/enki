from typing import Dict
from uuid import uuid4

from flask.testing import FlaskClient

from domain.messages.ports.task_repository import AlreadyExistingTaskUuid, NotFoundTask
from entrypoints.flask_app import app
from ..factories.task import task_factory
from ..helpers.filter import filter_dict_with_keys

BASE_PATH_TASK: str = "/api/enki/v1/tasks"


def test_add_task_then_recovers_it_and_recovers_all(app, client: FlaskClient):
    task1 = task_factory()
    add_task_response = post_add_task(client, task1)

    assert add_task_response.status_code == 201
    assert add_task_response.json['message'] == "Success"

    # fetching added task
    fetched_task1_response = get_task(client, task_uuid=task1["uuid"])
    assert fetched_task1_response.status_code == 200
    assert filter_dict_with_keys(fetched_task1_response.json["task"], task1) == task1

    # adding extra task
    task2 = task_factory()
    post_add_task(client, task2)

    # fetching all tasks
    fetched_all_tasks_response = get_all_tasks(client)
    assert fetched_all_tasks_response.status_code == 200
    assert [filter_dict_with_keys(task, task1) for task in fetched_all_tasks_response.json["tasks"]] == [task1,
                                                                                                         task2]


def test_already_exists_task(app, client: FlaskClient):
    task1 = task_factory()

    post_add_task(client, task1)

    add_already_exists_task_response = post_add_task(client, task1)
    assert add_already_exists_task_response.status_code == AlreadyExistingTaskUuid.code
    assert add_already_exists_task_response.json == {"message": AlreadyExistingTaskUuid.description}


def test_not_found_exists_task(app, client: FlaskClient):
    task1 = task_factory()

    post_add_task(client, task1)

    fetch_random_task_response = get_task(client, str(uuid4()))
    assert fetch_random_task_response.status_code == NotFoundTask.code
    assert fetch_random_task_response.json == {"message": NotFoundTask.description}


def post_add_task(client: FlaskClient, body: Dict[str, str]):
    return client.post(BASE_PATH_TASK, json=body)


def get_task(client: FlaskClient, task_uuid: str):
    return client.get(BASE_PATH_TASK + f"/{task_uuid}")


def get_all_tasks(client: FlaskClient):
    return client.get(BASE_PATH_TASK)
