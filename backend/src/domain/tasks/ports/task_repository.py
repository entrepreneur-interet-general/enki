import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.tag_repository import AbstractTagRepository

TasksList = List[TaskEntity]


class AlreadyExistingTaskUuid(HTTPException):
    code = 409
    description = "Task already exists"


class NotFoundTask(HTTPException):
    code = 404
    description = "Task not found"


class AlreadyExistingTagInThisTask(HTTPException):
    code = 409
    description = "Tag already exists in this task"


class NotFoundTagInThisTask(HTTPException):
    code = 404
    description = "Tag not found in this task"


class AbstractTaskRepository(abc.ABC):
    def __init__(self, tag_repo: AbstractTagRepository):
        self.tag_repo = tag_repo

    def add(self, task: TaskEntity) -> None:
        if self._match_uuid(task.uuid):
            raise AlreadyExistingTaskUuid()
        self._add(task)

    def get_by_uuid(self, uuid: str) -> TaskEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundTask
        return match

    def get_tag_by_task(self, uuid: str, tag_uuid: str) -> TagEntity:
        match = self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid)
        if not match:
            raise NotFoundTagInThisTask
        return match

    def add_tag_to_task(self, uuid: str, tag_uuid: str) -> None:
        match: TaskEntity = self.get_by_uuid(uuid)
        results = self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid)
        if self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid):
            print(self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid))
            raise AlreadyExistingTagInThisTask()
        tag: TagEntity = self.tag_repo.get_by_uuid(uuid=tag_uuid)
        self._add_tag_to_task(task=match, tag=tag)

    def remove_tag_to_task(self, uuid: str, tag_uuid: str) -> None:
        if not self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid):
            raise NotFoundTagInThisTask
        match: TaskEntity = self.get_by_uuid(uuid)
        tag: TagEntity = self.tag_repo.get_by_uuid(uuid=tag_uuid)
        self._remove_tag_to_task(match, tag=tag)

    @abc.abstractmethod
    def get_all(self) -> TasksList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[TaskEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_tag_by_task(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
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

    def _add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.append(tag)

    def _remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.remove(tag)

    def _get_tag_by_task(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        task: TaskEntity = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in task.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]
