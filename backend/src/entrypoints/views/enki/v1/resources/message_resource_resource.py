from flask import current_app
from flask_restful import Resource, reqparse
from typing import Dict, Any, Union, List
from domain.messages.services.message_service import MessageService
from domain.messages.services.resource_service import ResourceService


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
        ResourceService.delete_resource(uuid=resource_uuid,
                                        uow=current_app.context)
        return {"message": f"resource {resource_uuid} successfully deleted from message {uuid}"}, 202


class MessageMultipleResourceResource(WithMessageRepoResource):
    """Add, Delete and get specific message's resource
    ---
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
        - in: query
          name: resource_ids
          schema:
            type: array
            items: string
          required: true
          description: Resource Ids
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
        - in: query
          name: resource_ids
          schema:
            type: array
            items: string
          required: true
          description: Resource Ids
      responses:
        202:
          description: Successfully deleted relation
        404:
            description: relation not found

    """

    def put(self, uuid: str):
        parser = reqparse.RequestParser()
        parser.add_argument('resource_ids',
                            type=str,
                            help='Resource ids',
                            action='append', required=True)
        args = parser.parse_args()

        resource_ids: Union[str, List[str]] = args.get("resource_ids")
        if isinstance(resource_ids, str):
            resource_ids = [resource_ids]

        for resource_uuid in resource_ids:
            MessageService.add_resource_to_message(uuid,
                                                   resource_uuid=resource_uuid,
                                                   uow=current_app.context)

        return {"message": f"resources {resource_ids} successfully added from message {uuid}"}, 201

    def delete(self, uuid: str, resource_uuid: str):
        parser = reqparse.RequestParser()
        parser.add_argument('resource_ids',
                            type=str,
                            help='Resource ids',
                            action='append', required=True)
        args = parser.parse_args()

        resource_ids: Union[str, List[str]] = args.get("resource_ids")
        if isinstance(resource_ids, str):
            resource_ids = [resource_ids]
        for resource_uuid in resource_ids:
            MessageService.remove_resource_to_message(uuid,
                                                      resource_uuid=resource_uuid,
                                                      uow=current_app.context)
            ResourceService.delete_resource(uuid=resource_uuid,
                                            uow=current_app.context)
        return {"message": f"resources {resource_uuid} successfully deleted from message {uuid}"}, 202
