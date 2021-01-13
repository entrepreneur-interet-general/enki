from flask import current_app
from flask_restful import Resource
from typing import Dict, Any
from domain.messages.services.message_service import MessageService


class WithMessageRepoResource(Resource):
    def __init__(self):
        pass


class MessageResourceListResource(WithMessageRepoResource):
    """Get message's resources
    ---
    get:
      tags:
        - messages <> resources
      responses:
        200:
          description: Return a list of resources
          content:
            application/json:
              schema:
                type: array
                items: ResourceSchema
    """

    def get(self, uuid: str):
        resources = MessageService.list_resources(uuid, uow=current_app.context)
        return {"data": resources, "message": "success"}, 200


class MessageResourceResource(WithMessageRepoResource):
    """Add, Delete and get specific message's resource
    ---
    get:
      description: Building a relation between a tag and a message
      tags:
        - messages <> resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: resource_uuid
          schema:
            type: string
          required: true
          description: Resource id
      responses:
        200:
          description: Return relation

        404:
            description: relation not found
    put:
      description: Building a relation between a resource and a message
      tags:
        - messages <> resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: resource_uuid
          schema:
            type: string
          required: true
          description: Resource id
      responses:
        201:
          description: Successfully added relation
        404:
            description: relation not found
    delete:
      description: Deleting a relation between a resource and a message
      tags:
        - messages <> resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
        - in: path
          name: resource_uuid
          schema:
            type: string
          required: true
          description: Resource id
      responses:
        202:
          description: Successfully deleted relation
        404:
            description: relation not found

    """

    def get(self, uuid: str, resource_uuid: str):
        resource: Dict[str, Any] = MessageService.get_message_resource(uuid,
                                                                       resource_uuid=resource_uuid,
                                                                       uow=current_app.context)
        return {"data": resource, "message": "success"}, 200

    def put(self, uuid: str, resource_uuid: str):
        MessageService.add_resource_to_message(uuid,
                                               resource_uuid=resource_uuid,
                                               uow=current_app.context)
        return {"message": f"resource {resource_uuid} successfully added from message {uuid}"}, 201

    def delete(self, uuid: str, resource_uuid: str):
        MessageService.remove_resource_to_message(uuid,
                                                  resource_uuid=resource_uuid,
                                                  uow=current_app.context)
        return {"message": f"resource {resource_uuid} successfully deleted from message {uuid}"}, 202
