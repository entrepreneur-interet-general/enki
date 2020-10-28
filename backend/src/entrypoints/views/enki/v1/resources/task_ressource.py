from flask import request
from flask_restful import Resource

from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.services.task_service import TaskService


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
        return {
            "tasks":TaskService.list_tasks(self.taskRepo)
               }, 200

    def post(self):
        body = request.get_json()
        TaskService.add_task(body["uuid"], body["title"], body["description"], self.taskRepo)
        return {"message": "Success"}, 201


class TaskResource(WithTaskRepoResource):
    """All affairs list
        ---
        get:
          tags:
            - tasks
        """

    def get(self, uuid: str):
        return {
            "task": TaskService.get_by_uuid(uuid, self.taskRepo)
               }, 200
