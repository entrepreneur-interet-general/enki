from typing import Any, Dict, List
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository


class TaskService:
    @staticmethod
    def add_task(uuid: str, title: str, description: str, repo: AbstractTaskRepository):
        new_task = TaskEntity(uuid=uuid, title=title, description=description)
        repo.add(new_task)

    @staticmethod
    def add_tag_to_task(task_uuid, tag_uuid, repo: AbstractTaskRepository) -> None:
        repo.add_tag_to_task(task_uuid, tag_uuid)

    @staticmethod
    def remove_tag_to_task(task_uuid, tag_uuid, repo: AbstractTaskRepository) -> None:
        repo.remove_tag_to_task(task_uuid, tag_uuid)

    @staticmethod
    def list_tags(uuid: str, repo: AbstractTaskRepository) -> List[Dict[str, Any]]:
        task: TaskEntity = repo.get_by_uuid(uuid)
        return [tag.to_dict() for tag in task.tags]

    @staticmethod
    def list_tasks(repo: AbstractTaskRepository) -> List[Dict[str, Any]]:
        tasks: List[TaskEntity] = repo.get_all()
        serialized_tasks = [task.to_dict() for task in tasks]
        return serialized_tasks

    @staticmethod
    def get_by_uuid(uuid: str, repo: AbstractTaskRepository) -> Dict[str, Any]:
        task = repo.get_by_uuid(uuid)
        return task.to_dict()
