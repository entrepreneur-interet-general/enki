import dataclasses
from typing import List
from domain.entities.task_entity import TaskEntity
from adapters.task_repository.task_repository import AbstractTaskRepository


def add_task(title: str, *, repo: AbstractTaskRepository):
  new_task = TaskEntity(title)
  repo.add(new_task)

def list_tasks(repo: AbstractTaskRepository) -> List[TaskEntity]:
  return list(map(dataclasses.asdict, repo.get_all()))