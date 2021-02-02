from flask import request, current_app, g
from flask_restful import Resource, reqparse
from typing import Dict, Any, Union, List
from domain.messages.services.message_service import MessageService
from domain.messages.command import CreateMessage
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

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tags', type=str, help='Tags ids', action='append')
        parser.add_argument('evenement_id', type=str, help='Evenement id')
        args = parser.parse_args()
        tags: Union[str, List[str], None] = args.get("tags")
        evenement_id: Union[str, None] = args.get("evenement_id")
        if tags or evenement_id:
            messages = MessageService.list_messages_by_query(tag_ids=tags, evenement_id=evenement_id, uow=current_app.context)
        else:
            messages = MessageService.list_messages(current_app.context)

        return {
                   "data": messages,
                   "message": "success"
               }, 200

    def post(self):
        body = request.get_json()
        current_app.logger.info(f"body {body}")
        body["creator_id"] = g.user_info["id"]
        if g.user_info["fonction"] == "prefet":
            body["creator_position"] = f'{g.user_info["fonction"]}'
            body["creator_group"] = f'Préfecture {g.user_info["code_insee"]}'
        else:
            body["creator_position"] = f'{g.user_info["fonction"]}'
            body["creator_group"] = f'Mairie {g.user_info["code_insee"]}'

        command = CreateMessage(data=body)
        result = event_bus.publish(command, current_app.context)
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

    def get(self, uuid: str):
        return {
                   "data": MessageService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200

