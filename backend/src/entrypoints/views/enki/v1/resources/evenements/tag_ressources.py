from flask import request, current_app, g
from flask_restful import Resource

from domain.evenements.commands import CreateTag
from domain.evenements.services.tag_service import TagService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithTagRepoResource(Resource):
    def __init__(self):
        pass


class TagListResource(WithTagRepoResource):
    """Get all tags
    ---
    get:
      tags:
        - tags
      responses:
        200:
          description: Return a list of tags
          content:
            application/json:
              schema:
                type: array
                items: TagSchema
    post:
      description: Creating a tag
      tags:
        - tags
      requestBody:
        content:
          application/json:
            schema:  TagSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """

    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": TagService.list_tags(current_app.context),
                    "message": "success",
               }, 200

    def post(self):
        body = request.get_json()
        body["creator_id"] = g.user_info["id"]
        command = CreateTag(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class TagResource(WithTagRepoResource):
    """Get specific tag
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Tag id
      tags:
        - tags
      responses:
        200:
          description: Return specific tag
          content:
            application/json:
              schema: TagSchema
        404:
            description: Tag not found
    """

    def get(self, uuid: str):
        return {
                   "data": TagService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200
