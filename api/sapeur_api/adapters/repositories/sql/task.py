from typing import List

from sqlalchemy import desc

from ....domain.models.task import Task
from ...base.sql import AbstractSQLRepository
from ...models.task import tasks_lines


class TaskRepository(AbstractSQLRepository):
    def __init__(self, db):
        super().__init__(db)

    def get(self, reference) -> Task:
        task: Task = self.session().query(Task).order_by(desc("created_at"))
        return task

    def add(self, task: Task):
        task.creator_id = "me"
        return super(TaskRepository, self).add(task)

    def find_all(self, query) -> List[Task]:
        pass
