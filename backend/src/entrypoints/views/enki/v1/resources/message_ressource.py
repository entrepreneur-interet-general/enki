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
        - messages

    post:
      tags:
        - messages
    """

    def get(self):
        return {
                   "messages": MessageService.list_messages(current_app.context)
               }, 200

    def post(self):
        body = request.get_json()
        current_app.logger.info(f"body {body}")
        command = CreateMessage(data=body)
        result = event_bus.publish(command, current_app.context)
        return {
                   "message": "Success",
                   "message": result[0]
               }, 201


class MessageResource(WithMessageRepoResource):
    """Get specific message
    ---
    get:
      tags:
        - messages
    """

    def get(self, uuid: str):
        return {"message": MessageService.get_by_uuid(uuid, current_app.context),
                "result": "success"}, 200


class MessageTagListResource(WithMessageRepoResource):
    """Get message's tags
    ---
    get:
      tags:
        - messages
        - tags

    """

    def get(self, uuid: str):
        tags = MessageService.list_tags(uuid, uow=current_app.context)
        return {"tags": tags, "result": "success"}, 200


class MessageTagResource(WithMessageRepoResource):
    """Add, Delete and get specific message's tag
    ---
    put:
      tags:
        - messages
        - tags

    put:
      tags:
        - messages
        - tags

    delete:
      tags:
        - messages
        - tags
    """

    def get(self, uuid: str, tag_uuid: str):
        tag: Dict[str, Any] = MessageService.get_message_tag(uuid,
                                                             tag_uuid=tag_uuid,
                                                             uow=current_app.context)
        return {"tag": tag, "result": "Success"}, 200

    def put(self, uuid: str, tag_uuid: str):
        MessageService.add_tag_to_message(uuid,
                                          tag_uuid=tag_uuid,
                                          uow=current_app.context)
        return {"result": f"tag {tag_uuid} successfully added from message {uuid}"}, 201

    def delete(self, uuid: str, tag_uuid: str):
        MessageService.remove_tag_to_message(uuid,
                                             tag_uuid=tag_uuid,
                                             uow=current_app.context)
        return {"result": f"tag {tag_uuid} successfully deleted from message {uuid}"}, 202
