from domain.tasks.ports.task_repository import AlreadyExistingTaskUuid, InMemoryTaskRepository, NotFoundTask
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.services.task_service import TaskService
from uuid import uuid4
import pytest


def initiateRepo():
    return InMemoryTaskRepository()


def test_add_task():
    repo = initiateRepo()
    uuid = str(uuid4())
    expected_title = "My title"
    expected_description = "My description"
    TaskService.add_task(uuid,
                         title=expected_title,
                         description=expected_description,
                         repo=repo)

    print(repo.tasks[0])
    assert repo.tasks[0] == TaskEntity(uuid=uuid,
                                       title=expected_title,
                                       description=expected_description)


def test_fails_to_add_task_when_already_exists():
    repo = initiateRepo()

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
    repo.set_tasks([task1])

    with pytest.raises(AlreadyExistingTaskUuid):
        TaskService.add_task(task1_uuid, "Some title", "Some description", repo=repo)


def test_list_tasks():
    repo = initiateRepo()
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
    repo.set_tasks([task1])

    tasks = TaskService.list_tasks(repo)

    assert len(tasks) == 1
    assert {k: v for k, v in tasks[0].items() if k in serialized_task1} == serialized_task1


def test_get_by_uuid_when_not_present():
    repo = initiateRepo()
    with pytest.raises(NotFoundTask):
        TaskService.get_by_uuid("not_in_repo_uuid", repo)


def test_get_by_uuid_when_task_present():
    repo = initiateRepo()

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
    repo.set_tasks([task1])

    task = TaskService.get_by_uuid(task1_uuid, repo)
    assert {k: v for k, v in task.items() if k in serialized_task1} == serialized_task1
