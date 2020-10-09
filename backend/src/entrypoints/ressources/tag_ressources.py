import uuid

from flask import request
from flask_restful import Resource

from domain.tags.ports.tag_repository import AbstractTagRepository
from domain.tags.tag_service import TagService


class WithTagRepoResource(Resource):
    def __init__(self, tag_repo: AbstractTagRepository):
        self.tag_repo = tag_repo


class TagListResource(WithTagRepoResource):
    def get(self):
        return TagService.list_tags(self.tag_repo), 200

    def post(self):
        body = request.get_json()
        TagService.add_tag(
            uuid=body.get("uuid"),
            title=body.get("title"),
            description=body.get("description"),
            color=body.get("color"),
            repo=self.tag_repo
        )
        return {"message": "Success"}, 201


class TagResource(WithTagRepoResource):
    def get(self, uuid: str):
        return TagService.get_by_uuid(uuid, self.tag_repo)