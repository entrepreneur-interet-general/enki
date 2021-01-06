from typing import Any, Dict, List

from flask import current_app

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.schema import TaskSchema, TagSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class TaskService:
    schema = TaskSchema

    @staticmethod
    def add_task(data: Dict[str, Any], uow: AbstractUnitOfWork) -> Dict[str, Any]:
        task: TaskEntity = TaskService.schema().load(data)
        current_app.logger.info("TaskDeserialized")
        current_app.logger.info(task)
        current_app.logger.info(task.created_at)
        return_value = TaskService.schema().dump(task)
        with uow:
            uow.task.add(task)
        return return_value

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
            return TagSchema(many=True).dump(task.tags)

    @staticmethod
    def get_task_tag(uuid: str, tag_uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            tag: TagEntity = uow.task.get_tag_by_task(uuid=uuid, tag_uuid=tag_uuid)
            return TagSchema().dump(tag)

    @staticmethod
    def list_tasks(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            tasks: List[TaskEntity] = uow.task.get_all()
            return TaskService.schema(many=True).dump(tasks)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            task = uow.task.get_by_uuid(uuid)
            return TaskService.schema().dump(task)
