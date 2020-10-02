from typing import Any, List
from adapters.task_repository.task_repository import AbstractTaskRepository
from domain.entities.task_entity import TaskEntity

class PgTaskRepository(AbstractTaskRepository):
    def __init__(self, session: Any):
        self.session = session

    def add(self, task: TaskEntity):
        self.session.add(task)
        self.session.commit()

    def get_by_uuid(self, uuid: str):
        self.session.query()

    def get_all(self) -> List[TaskEntity]:
        return self.session.query(TaskEntity)