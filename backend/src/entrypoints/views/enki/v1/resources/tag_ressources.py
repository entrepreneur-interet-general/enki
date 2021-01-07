from flask import request, current_app
from flask_restful import Resource

from domain.tasks.command import CreateTag
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.services.tag_service import TagService
from entrypoints.extensions import event_bus


class WithTagRepoResource(Resource):
    def __init__(self):
        pass


class TagListResource(WithTagRepoResource):
    """Get all tags
    ---
    get:
      tags:
        - tags

    post:
      tags:
        - tags
    """

    def get(self):
        return {"tags": TagService.list_tags(current_app.context)}, 200

    def post(self):
        body = request.get_json()
        command = CreateTag(data=body)
        result = event_bus.publish(command, current_app.context)
        return {"message": "Success",
                "tag": result[0]}, 201


class TagResource(WithTagRepoResource):
    """Get specific tag
    ---
    get:
      tags:
        - tags
    """

    def get(self, uuid: str):
        return {"tag": TagService.get_by_uuid(uuid, current_app.context)}, 200
