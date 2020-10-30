from flask import request, current_app
from flask_restful import Resource

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.services.tag_service import TagService


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
        return {"tags": TagService.list_tags(current_app.context.tag)}, 200

    def post(self):
        body = request.get_json()
        TagService.add_tag(
            uuid=body.get("uuid"),
            title=body.get("title"),
            description=body.get("description"),
            color=body.get("color"),
            repo=current_app.context.tag
        )
        return {"message": "Success"}, 201


class TagResource(WithTagRepoResource):
    """Get specific tag
    ---
    get:
      tags:
        - tags
    """

    def get(self, uuid: str):
        return {"tag": TagService.get_by_uuid(uuid, current_app.context.tag)}, 200
