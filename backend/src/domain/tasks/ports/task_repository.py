import abc
from typing import List, Union

from domain.tasks.entities.task_entity import TaskEntity

TasksList = List[TaskEntity]

class AlreadyExistingTaskUuid(Exception):
    pass

class NotFoundTask(Exception):
  pass

class AbstractTaskRepository(abc.ABC):
    def add(self, task: TaskEntity) -> None:
        if self._match_uuid(task.uuid):
            raise AlreadyExistingTaskUuid()
        self._add(task)

    def get_by_uuid(self, uuid : str) -> TaskEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundTask
        return matches[0]

    @abc.abstractclassmethod
    def get_all(self) -> TasksList:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _match_uuid(self, uuid: str) -> List[TaskEntity]:
        raise NotImplementedError



class InMemoryTaskRepository(AbstractTaskRepository):
    _tasks: TasksList = []

    def get_all(self) -> TasksList:
        return self._tasks

    def _match_uuid(self, uuid: str) -> List[TaskEntity]:
        return [task for task in self._tasks if task.uuid == uuid]

    def _add(self, task: TaskEntity):
        self._tasks.append(task)

    # next methods are only for test purposes
    @property
    def tasks(self) -> TasksList:
        return self._tasks

    def set_tasks(self, tasks: TasksList) -> None:
        self._tasks = tasks