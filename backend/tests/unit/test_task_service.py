from adapters.task_repository.task_repository import InMemoryTaskRepository
from domain.entities.task_entity import TaskEntity
from service_layer.task_service import add_task, list_tasks
from uuid import uuid4

def initiateRepo():
  return InMemoryTaskRepository()

def test_add_task():
  repo = initiateRepo()
  uuid = str(uuid4())
  expected_title = "My title"
  add_task(uuid, expected_title, repo=repo)

  assert repo.tasks[0] == TaskEntity(uuid, expected_title)

def test_list_tasks():
  repo = initiateRepo()
  serialized_task1 = {
    "uuid": str(uuid4()),
    "title": "Task 1 title"
  }
  task1 = TaskEntity(serialized_task1["uuid"], serialized_task1["title"])
  repo.set_tasks([task1])

  tasks = list_tasks(repo)

  assert len(tasks) == 1
  assert tasks[0] == serialized_task1



