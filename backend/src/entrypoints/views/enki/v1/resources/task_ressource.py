from flask import request, current_app
from flask_restful import Resource
from typing import Dict, Any

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.services.task_service import TaskService


class WithTaskRepoResource(Resource):
    def __init__(self):
        pass


class TaskListResource(WithTaskRepoResource):
    """Get all tasks
    ---
    get:
      tags:
        - tasks

    post:
      tags:
        - tasks
    """

    def get(self):
        return {
                   "tasks": TaskService.list_tasks(current_app.context.task)
               }, 200

    def post(self):
        body = request.get_json()
        TaskService.add_task(uuid=body.get("uuid"),
                             title=body["title"],
                             description=body.get("description"),
                             repo=current_app.context.task)
        return {"message": "Success"}, 201


class TaskResource(WithTaskRepoResource):
    """Get specific task
    ---
    get:
      tags:
        - tasks
    """

    def get(self, uuid: str):
        return {"task": TaskService.get_by_uuid(uuid, current_app.context.task), "message": "success"}, 200


class TaskTagListResource(WithTaskRepoResource):
    """Get task's tags
    ---
    get:
      tags:
        - tasks
        - tags

    """

    def get(self, uuid: str):
        tags = TaskService.list_tags(uuid, repo=current_app.context.task)
        return {"tags": tags, "message": "success"}, 200


class TaskTagResource(WithTaskRepoResource):
    """Add, Delete and get specific task's tag
    ---
    put:
      tags:
        - tasks
        - tags

    put:
      tags:
        - tasks
        - tags

    delete:
      tags:
        - tasks
        - tags
    """

    def get(self, uuid: str, tag_uuid: str):
        tag: Dict[str, Any] = TaskService.get_task_tag(uuid,
                                                       tag_uuid=tag_uuid,
                                                       repo=current_app.context.task)
        return {"tag": tag, "message": "Success"}, 200

    def put(self, uuid: str, tag_uuid: str):
        TaskService.add_tag_to_task(uuid,
                                    tag_uuid=tag_uuid,
                                    repo=current_app.context.task)
        return {"message": f"tag {tag_uuid} successfully added from task {uuid}"}, 201

    def delete(self, uuid: str, tag_uuid: str):
        TaskService.remove_tag_to_task(uuid,
                                       tag_uuid=tag_uuid,
                                       repo=current_app.context.task)
        return {"message": f"tag {tag_uuid} successfully deleted from task {uuid}"}, 202
