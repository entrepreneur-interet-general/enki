import abc
from typing import List, Union
from domain.entities.task_entity import TaskEntity

class AbstractTaskRepository(abc.ABC):
    def add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    def get_by_uuid(self, uuid : str) -> Union[TaskEntity,None]:
        raise NotImplementedError

    def get_all(self) -> List[TaskEntity]:
        raise NotImplementedError


Tasks = List[TaskEntity]

class InMemoryTaskRepository(AbstractTaskRepository):
    _tasks: Tasks = []

    def add(self, task: TaskEntity) -> None:
        self._tasks.append(task)

    def get_by_uuid(self, uuid : str) -> Union[TaskEntity,None] :
        return next(task for task in self._tasks if task['uuid'] == uuid)

    def get_all(self) -> List[TaskEntity]:
        return self._tasks

    @property
    def tasks(self) -> Tasks:
        return self._tasks

    def set_tasks(self, tasks: Tasks) -> None:
        self._tasks = tasks