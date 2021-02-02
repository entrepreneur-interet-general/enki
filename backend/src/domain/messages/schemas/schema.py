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
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

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
    severity = EnumField(Severity, validate=validate.OneOf([e.value for e in Severity]))
    type = EnumField(MessageType, validate=validate.OneOf([e.value for e in MessageType]))
    creator_id = fields.Str(required=False)
    creator_name = fields.Str(required=False)
    started_at = fields.DateTime(required=False)
    tags = fields.Nested(TagSchema, required=False, many=True, dump_only=True)
    tag_ids = fields.List(fields.Str(), required=False, load_only=True, many=True)
    resources = fields.Nested(ResourceSchema, required=False, many=True, dump_only=True)
    resource_ids = fields.List(fields.Str(), required=False, load_only=True, many=True)
    event_type = fields.Str(missing="task")
    executor_id = fields.Str(required=False)
    # executor_type = fields.Str(required=False)
    done_at = fields.DateTime(default=None, dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.now(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.now(), dump_only=True)

    @post_load
    def make_message(self, data: dict, **kwargs):
        entity = MessageEntity.from_dict(data)
        return entity

    def handle_error(self, exc, data, **kwargs):
        raise MessageValidationError(description=exc.normalized_messages())