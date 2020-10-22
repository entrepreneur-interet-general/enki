from flask import request
from flask_restful import Resource

from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.task_service import add_task, list_tasks, get_by_uuid


class WithTaskRepoResource(Resource):
    def __init__(self, taskRepo: AbstractTaskRepository):
        self.taskRepo = taskRepo


class TaskListResource(WithTaskRepoResource):
    """All affairs list
        ---
        get:
          tags:
            - tasks
        post:
          tags:
            - tasks
        """
    def get(self):
        return list_tasks(self.taskRepo), 200

    def post(self):
        body = request.get_json()
        add_task(body["uuid"], body["title"], self.taskRepo)
        return {"message": "Success"}, 201


class TaskResource(WithTaskRepoResource):
    """All affairs list
        ---
        get:
          tags:
            - tasks
        """
    def get(self, uuid: str):
        return get_by_uuid(uuid, self.taskRepo)
