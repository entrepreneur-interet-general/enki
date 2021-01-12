from flask import request, current_app
from flask_restful import Resource
from typing import Dict, Any
from domain.messages.services.message_service import MessageService
from domain.messages.command import CreateMessage
from entrypoints.extensions import event_bus


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
        400:
          description: bad request, bad parameters
    """

    def get(self):
        return {
                   "data": MessageService.list_messages(current_app.context),
                   "message": "success",
               }, 200

    def post(self):
        body = request.get_json()
        current_app.logger.info(f"body {body}")
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

