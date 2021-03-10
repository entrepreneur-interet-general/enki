from typing import Union, List

from flask import request, current_app, g
from flask_restful import Resource, reqparse

from domain.evenements.commands import CreateMessage
from domain.evenements.services.evenement_service import EvenementService
from entrypoints.extensions import event_bus
from entrypoints.middleware import user_info_middleware


class WithMessageRepoResource(Resource):
    def __init__(self):
        pass


class MessageListResource(WithMessageRepoResource):
    """Get all messages
    ---
    get:
      tags:
        - message
      responses:
        200:
          description: Return a list of messages
          content:
            application/json:
              schema:
                type: array
                items: MessageSchema
      parameters:
        - in: query
          name: tags
          schema:
            type: array
            items:
              type: string
          description: Tag id or list of tag ids
        - in: query
          name: evenement_id
          schema:
            type: str
          description: Evenement ID
    post:
      description: Creating a message
      tags:
        - message
      requestBody:
        content:
          application/json:
            schema:  MessageSchema
      responses:
        201:
          description: Successfully created
          content:
            application/json:
              schema: MessageSchema
        400:
          description: bad request, bad parameters
    """
    method_decorators = [user_info_middleware]

    def get(self, uuid: str):
        parser = reqparse.RequestParser()
        parser.add_argument('tags', type=str, help='Tags ids', action='append')
        args = parser.parse_args()
        tags: Union[str, List[str], None] = args.get("tags")
        if tags:
            messages = EvenementService.list_messages_by_query(uuid=uuid, tag_ids=tags,  uow=current_app.context)
        else:
            messages = EvenementService.list_messages(uuid=uuid, uow=current_app.context)

        return {
                   "data": messages,
                   "message": "success"
               }, 200

    def post(self, uuid: str):
        current_app.logger.info(f"Start after post")
        body = request.get_json()
        current_app.logger.info(f"body {body}")
        body["creator_id"] = g.user_info["id"]
        body["evenement_id"] = uuid
        command = CreateMessage(data=body)
        result = event_bus.publish(command, current_app.context)
        current_app.logger.info("test")
        return {
                   "message": "success",
                   "data": result[0]
               }, 201


class MessageResource(WithMessageRepoResource):
    """Get specific message
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Message id
      tags:
        - message
      responses:
        200:
          description: Return a list of messages
          content:
            application/json:
              schema: MessageSchema
    """

    def get(self, uuid: str, message_uuid: str):
        return {
                   "data": EvenementService.get_message_by_uuid(uuid=uuid, message_uuid=message_uuid, uow=current_app.context),
                   "message": "success"
               }, 200

