from domain.tasks.ports.task_repository import AlreadyExistingTaskUuid, InMemoryTaskRepository, NotFoundTask
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.task_service import add_task, get_by_uuid, list_tasks
from uuid import uuid4
import pytest

def initiateRepo():
  return InMemoryTaskRepository()

def test_add_task():
  repo = initiateRepo()
  uuid = str(uuid4())
  expected_title = "My title"
  add_task(uuid, expected_title, repo=repo)

  assert repo.tasks[0] == TaskEntity(uuid, expected_title)

def test_fails_to_add_task_when_already_exists():
  repo = initiateRepo()

  task1_uuid = str(uuid4())
  serialized_task1 = {
    "uuid": task1_uuid,
    "title": "Task 1 title"
  }
  task1 = TaskEntity(task1_uuid, serialized_task1["title"])
  repo.set_tasks([task1])

  with pytest.raises(AlreadyExistingTaskUuid):
    add_task(task1_uuid, "Some title", repo=repo)



def test_list_tasks():
  repo = initiateRepo()
  task1_uuid = str(uuid4())
  serialized_task1 = {
    "uuid": task1_uuid,
    "title": "Task 1 title"
  }
  task1 = TaskEntity(task1_uuid, serialized_task1["title"])
  repo.set_tasks([task1])

  tasks = list_tasks(repo)

  assert len(tasks) == 1
  assert tasks[0] == serialized_task1

def test_get_by_uuid_when_not_present():
  repo = initiateRepo()
  with pytest.raises(NotFoundTask):
    get_by_uuid("not_in_repo_uuid", repo)

def test_get_by_uuid_when_task_present():
  repo = initiateRepo()

  task1_uuid = str(uuid4())
  serialized_task1 = {
    "uuid": task1_uuid,
    "title": "Task 1 title"
  }
  task1 = TaskEntity(task1_uuid, serialized_task1["title"])
  repo.set_tasks([task1])

  task = get_by_uuid(task1_uuid, repo)

  assert task == serialized_task1
