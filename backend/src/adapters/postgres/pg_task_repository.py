from typing import Any, List

from sqlalchemy.orm.session import Session
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.entities.task_entity import TaskEntity

class PgTaskRepository(AbstractTaskRepository):
    def get_all(self) -> List[TaskEntity]:
        return self.session.query(TaskEntity).all()


    def __init__(self, session: Session):
        self.session = session

    def _add(self, task: TaskEntity):
        self.session.add(task)
        self.session.commit()

    def _match_uuid(self, uuid: str):
        return self.session.query(TaskEntity).filter(TaskEntity.uuid == uuid).all()