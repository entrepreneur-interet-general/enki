from domain.messages.entities.task_entity import TaskEntity
from domain.messages.ports.task_repository import AlreadyExistingTaskUuid, NotFoundTask, \
    AbstractTaskRepository
from domain.messages.services.task_service import TaskService
from tests.helpers.filter import filter_dict_with_keys
from uuid import uuid4
import pytest


def test_add_task(task_repo: AbstractTaskRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    expected_event = "event_id"
    task = TaskEntity(uuid,
                         title=expected_title,
                         description=expected_description,
                        evenement_id=expected_event
                      )
    task_repo.add(task)

    assert task_repo.get_all()[0] == task


def test_fails_to_add_task_when_already_exists(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description",
        "evenement_id":"event_id"
    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       evenement_id=serialized_task1["evenement_id"],
                       )
    task_repo.add(task1)

    with pytest.raises(AlreadyExistingTaskUuid):
        task_repo.add(task1)


def test_list_tasks(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description",
        "evenement_id": "event_id"
    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       evenement_id=serialized_task1["evenement_id"],

                       )
    task_repo.add(task1)

    tasks = task_repo.get_all()

    assert len(tasks) == 1
    assert tasks[0] == task1


def test_get_by_uuid_when_not_present(task_repo: AbstractTaskRepository):
    with pytest.raises(NotFoundTask):
        task_repo.get_by_uuid("not_in_repo_uuid")


def test_get_by_uuid_when_task_present(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description",
        "evenement_id": "event_id"

    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       evenement_id=serialized_task1["evenement_id"],

                       )
    task_repo.add(task1)

    task = task_repo.get_by_uuid(task1_uuid)
    assert task == task1
