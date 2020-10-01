import abc
from typing import Dict, List, Union
from domain.entities.task_entity import TaskEntity

class AbstractTaskRepository(abc.ABC):
    def __init__(self):
        pass

    def add(self, task: TaskEntity) -> None:
        raise NotImplementedError

    def get_by_uuid(self, uuid : str) -> Union[TaskEntity,None]:
        raise NotImplementedError

    def get_all(self) -> List[TaskEntity]:
        raise NotImplementedError


class InMemoryTaskRepository(AbstractTaskRepository):
    tasks: Dict[str, TaskEntity] = {}

    def add(self, task: TaskEntity) -> None:
        self.tasks[task.uuid] = task

    def get_by_uuid(self, uuid : str) -> Union[TaskEntity,None] :
        return self.tasks.get(uuid)

    def get_all(self) -> List[TaskEntity]:
        return list(self.tasks.values())