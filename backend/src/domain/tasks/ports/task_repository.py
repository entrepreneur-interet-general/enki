import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity

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

    def add(self, task: TaskEntity) -> None:
        if self._match_uuid(task.uuid):
            raise AlreadyExistingTaskUuid()
        self._add(task)

    def get_by_uuid(self, uuid: str) -> TaskEntity:
        match = self._match_uuid(uuid)
        if not match:
            raise NotFoundTask
        return match

    def get_by_uuid_list(self, uuids: List[str]) -> TasksList:
        matches = self._match_uuids(uuids)
        if not matches:
            raise NotFoundTask
        return matches

    def get_tag_by_task(self, uuid: str, tag_uuid: str) -> TagEntity:
        match = self._get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid)
        if not match:
            raise NotFoundTagInThisTask()
        return match

    def get_tags(self, uuid: str):
        match = self.get_by_uuid(uuid=uuid)
        if not match:
            raise NotFoundTagInThisTask
        return match.tags

    @abc.abstractmethod
    def get_all(self) -> TasksList:
        raise NotImplementedError

    @abc.abstractmethod
    def _add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[TaskEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuids(self, uuids: List[str]) -> TasksList:
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

    def add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.append(tag)

    def remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.remove(tag)

    def _get_tag_by_task(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        task: TaskEntity = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in task.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> TasksList:
        matches = [task for task in self._tasks if task.uuid in uuids]
        return matches
