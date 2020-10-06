from typing import Any, List
from adapters.task_repository.task_repository import AbstractTaskRepository
from domain.tasks.entities.task_entity import TaskEntity

class PgTaskRepository(AbstractTaskRepository):
    def __init__(self, session: Any):
        self.session = session

    def _add(self, task: TaskEntity):
        self.session.add(task)
        self.session.commit()

    def _match_uuid(self, uuid: str):
        return self.session.query(TaskEntity).filter(TaskEntity.uuid == uuid)

    def get_all(self) -> List[TaskEntity]:
        return self.session.query(TaskEntity)