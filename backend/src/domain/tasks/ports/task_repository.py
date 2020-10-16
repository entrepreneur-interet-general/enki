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

    def get_by_uuid(self, uuid: str) -> TaskEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundTask
        return match

    def add_tag_to_task(self, uuid: str, tag_uuid: str) -> None:
        match = self._match_uuid(uuid)
        self._add_tag_to_task(match, tag_uuid=tag_uuid)

    def remove_tag_to_task(self, uuid: str, tag_uuid: str) -> None:
        match = self._match_uuid(uuid)
        self._remove_tag_to_task(match, tag_uuid=tag_uuid)

    @abc.abstractclassmethod
    def get_all(self) -> TasksList:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _add_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _remove_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def _match_uuid(self, uuid: str)-> Union[TaskEntity, None]:
        raise NotImplementedError


class InMemoryTaskRepository(AbstractTaskRepository):
    _tasks: TasksList = []

    def get_all(self) -> TasksList:
        return self._tasks

    def _match_uuid(self, uuid: str) -> Union[TaskEntity, None]:
        matches = [task for task in self._tasks if task.uuid == uuid]
        if not matches:
            return None
        return matches[0]

    def _add(self, task: TaskEntity):
        self._tasks.append(task)

    # next methods are only for test purposes
    @property
    def tasks(self) -> TasksList:
        return self._tasks

    def set_tasks(self, tasks: TasksList) -> None:
        self._tasks = tasks

    def _add_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        # TODO: fill _add_tag_to_task for inmemory repository
        raise NotImplementedError

    def _remove_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        # TODO: fill _remove_tag_to_task for inmemory repository
        raise NotImplementedError
