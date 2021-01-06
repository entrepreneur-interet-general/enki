from typing import Any, Dict, List
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from service_layer.unit_of_work import AbstractUnitOfWork


class TaskService:
    @staticmethod
    def add_task(uuid: str, title: str, description: str, uow: AbstractUnitOfWork):
        new_task = TaskEntity(uuid=uuid, title=title, description=description)
        with uow:
            uow.task.add(new_task)

    @staticmethod
    def add_tag_to_task(task_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            uow.task.add_tag_to_task(task_uuid, tag_uuid)

    @staticmethod
    def remove_tag_to_task(task_uuid, tag_uuid, uow: AbstractUnitOfWork) -> None:
        with uow:
            uow.task.remove_tag_to_task(task_uuid, tag_uuid)

    @staticmethod
    def list_tags(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            task: TaskEntity = uow.task.get_tags(uuid)
            return [tag.to_dict() for tag in task.tags]

    @staticmethod
    def get_task_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag: TagEntity = uow.task.get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid)
            return tag.to_dict()

    @staticmethod
    def list_tasks(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            tasks: List[TaskEntity] = uow.task.get_all()
            serialized_tasks = [task.to_dict() for task in tasks]
            return serialized_tasks

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            task = uow.task.get_by_uuid(uuid)
            return task.to_dict()
