from typing import Any, Dict, List
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.task_repository import AbstractTaskRepository

def add_task(uuid: str, title: str, repo: AbstractTaskRepository):
  new_task = TaskEntity(uuid, title)
  repo.add(new_task)

def list_tasks(repo: AbstractTaskRepository) -> List[Dict[str, Any]]:
  tasks = repo.get_all()
  serialized_tasks = [task.asdict() for task in tasks]
  return serialized_tasks

def get_by_uuid(uuid: str, repo: AbstractTaskRepository) -> Dict[str, Any]:
  task = repo.get_by_uuid(uuid)
  return task.asdict()