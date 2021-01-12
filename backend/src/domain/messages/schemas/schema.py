from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from datetime import datetime
from werkzeug.exceptions import HTTPException
from domain.messages.entities.tag_entity import TagEntity
from domain.messages.entities.message_entity import MessageEntity, MessageType, Severity
from domain.messages.schemas.resource_schema import ResourceSchema


class MessageValidationError(HTTPException):
    code = 400


class TagValidationError(HTTPException):
    code = 400


class TagSchema(Schema):
    __model__ = TagEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=5))
    creator_id = fields.Str(required=False)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_tag(self, data: dict, **kwargs):
        return TagEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise TagValidationError(description=exc.normalized_messages())


class MessageSchema(Schema):
    __model__ = MessageEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=5))
    description = fields.Str(required=True, validate=validate.Length(min=5))
    evenement_id = fields.Str(required=True)
    severity = EnumField(Severity)
    type = EnumField(MessageType, by_value=True)
    creator_id: fields.Str(required=False)
    started_at: fields.DateTime()
    tags = fields.Nested(TagSchema, required=False, many=True)
    resources = fields.Nested(ResourceSchema, required=False, many=True)
    event_type = fields.Str(missing="task")
    executor_id = fields.Str(required=False)
    # executor_type = fields.Str(required=False)
    done_at = fields.DateTime(default=None)
    created_at = fields.DateTime(missing=lambda: datetime.now())
    updated_at = fields.DateTime(missing=lambda: datetime.now())

    @post_load
    def make_message(self, data: dict, **kwargs):
        entity = MessageEntity.from_dict(data)
        return entity

    def handle_error(self, exc, data, **kwargs):
        raise MessageValidationError(description=exc.normalized_messages())