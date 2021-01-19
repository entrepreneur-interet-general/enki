from flask import request, current_app
from flask_restful import Resource
from domain.messages.command import CreateResource
from domain.messages.services.resource_service import ResourceService
from entrypoints.extensions import event_bus


class WithResourceRepoResource(Resource):
    def __init__(self):
        pass


class ResourceListResource(WithResourceRepoResource):
    """Get all resources
    ---
    post:
      description: Creating a resource
      tags:
        - resources
      requestBody:
        content:
          application/json:
            schema:  ResourceSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters

    """

    def post(self):
        body = request.get_json()
        create_command = CreateResource(data=body)
        result = event_bus.publish(create_command, current_app.context)
        return {"message": "success",
                "data": result[0]}, 201


class ResourceResource(WithResourceRepoResource):
    """Get specific resource
    ---
    get:
      tags:
        - resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        200:
          description: Return specific resource
          content:
            application/json:
              schema: ResourceSchema
        404:
            description: Resource not found
    """

    def get(self, uuid: str):
        return {
                   "data": ResourceService.get_resource(uuid, current_app.context),
                   "message": "success"
               }, 200
