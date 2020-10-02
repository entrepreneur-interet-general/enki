import dataclasses
from typing import Any, Dict, List
from domain.entities.task_entity import TaskEntity
from adapters.task_repository.task_repository import AbstractTaskRepository


def add_task(uuid: str, title: str, *, repo: AbstractTaskRepository):
  new_task = TaskEntity(uuid, title)
  repo.add(new_task)

def list_tasks(repo: AbstractTaskRepository) -> List[Dict[str, Any]]:
  tasks = repo.get_all()
  serialized_tasks = list(map(dataclasses.asdict, tasks))
  return serialized_tasks