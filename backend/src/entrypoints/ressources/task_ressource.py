from flask import request
from flask_restful import Resource

from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tags.ports.tag_repository import AbstractTagRepository
from domain.tasks.task_service import TaskService


class WithTaskRepoResource(Resource):
    def __init__(self, task_repo: AbstractTaskRepository, tag_repo: AbstractTagRepository = None):
        self.task_repo = task_repo
        self.tag_repo = tag_repo


class TaskListResource(WithTaskRepoResource):
    def get(self):
        return TaskService.list_tasks(self.task_repo), 200

    def post(self):
        body = request.get_json()
        TaskService.add_task(uuid=body.get("uuid"), title=body["title"], repo=self.task_repo)
        return {"message": "Success"}, 201


class TaskResource(WithTaskRepoResource):
    def get(self, uuid: str):
        return {"task": TaskService.get_by_uuid(uuid, self.task_repo), "message": "success"}, 200


class TaskTagResource(WithTaskRepoResource):
    def put(self, uuid: str, tag_uuid: str):
        TaskService.add_tag_to_task(uuid,
                                    tag_uuid=tag_uuid,
                                    task_repo=self.task_repo,
                                    tag_repo=self.tag_repo)
        return {"message": f"tag {tag_uuid} successfully added to task {uuid}"}, 204

    def delete(self, uuid: str, tag_uuid: str):
        TaskService.remove_tag_to_task(uuid,
                                       tag_uuid=tag_uuid,
                                       task_repo=self.task_repo,
                                       tag_repo=self.tag_repo)
