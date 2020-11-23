from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.task_repository import AlreadyExistingTaskUuid, NotFoundTask, \
    AbstractTaskRepository
from domain.tasks.services.task_service import TaskService
from ..helpers.filter import filter_dict_with_keys
from uuid import uuid4
import pytest


def test_add_task(task_repo: AbstractTaskRepository):
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    TaskService.add_task(uuid,
                         title=expected_title,
                         description=expected_description,
                         repo=task_repo)

    print(task_repo.get_all()[0])
    print(uuid)
    assert task_repo.get_all()[0] == TaskEntity(uuid=uuid,
                                            title=expected_title,
                                            description=expected_description)


def test_fails_to_add_task_when_already_exists(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description",
    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       )
    task_repo.add(task1)

    with pytest.raises(AlreadyExistingTaskUuid):
        TaskService.add_task(task1_uuid, "Some title", "Some description", repo=task_repo)


def test_list_tasks(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description",
    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       )
    task_repo.add(task1)

    tasks = TaskService.list_tasks(task_repo)

    assert len(tasks) == 1
    assert filter_dict_with_keys(tasks[0], serialized_task1) == serialized_task1


def test_get_by_uuid_when_not_present(task_repo: AbstractTaskRepository):
    with pytest.raises(NotFoundTask):
        TaskService.get_by_uuid("not_in_repo_uuid", task_repo)


def test_get_by_uuid_when_task_present(task_repo: AbstractTaskRepository):
    task1_uuid = str(uuid4())
    serialized_task1 = {
        "uuid": task1_uuid,
        "title": "Task 1 title",
        "description": "Task 1 description"
    }
    task1 = TaskEntity(uuid=task1_uuid,
                       title=serialized_task1["title"],
                       description=serialized_task1["description"],
                       )
    task_repo.add(task1)

    task = TaskService.get_by_uuid(task1_uuid, task_repo)
    assert filter_dict_with_keys(task, serialized_task1) == serialized_task1
