from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.tasks.entities.info_entity import InformationEntity
from domain.tasks.entities.message_entity import MessageEventEntity, Severity
from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity, TaskType


class TaskValidationError(HTTPException):
    code = 400


class TagValidationError(HTTPException):
    code = 400


class InformationValidationError(HTTPException):
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


class MessageEventEntitySchema(Schema):
    __model__ = MessageEventEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=5))
    description = fields.Str(required=True, validate=validate.Length(min=5))
    evenement_id = fields.Str(required=True)
    severity = EnumField(Severity)
    creator_id: fields.Str(required=False)
    started_at: fields.DateTime()
    tags = fields.Nested(TagSchema, required=False, many=True)
    created_at = fields.DateTime(missing=lambda: datetime.now())
    updated_at = fields.DateTime(missing=lambda: datetime.now())


class TaskSchema(MessageEventEntitySchema):
    __model__ = TaskEntity

    type = EnumField(TaskType, by_value=True)
    event_type = fields.Str(missing="task")
    executor_id = fields.Str(required=False)
    # executor_type = fields.Str(required=False)
    done_at = fields.DateTime(default=None)

    @post_load
    def make_task(self, data: dict, **kwargs):
        current_app.logger.info("make_task")
        current_app.logger.info(data)
        entity = TaskEntity.from_dict(data)
        current_app.logger.info(entity.created_at)

        return entity

    def handle_error(self, exc, data, **kwargs):
        raise TaskValidationError(description=exc.normalized_messages())


class InformationSchema(MessageEventEntitySchema):
    __model__ = InformationEntity
    type = EnumField(TaskType, by_value=True)
    event_type = fields.Str(missing="information")

    @post_load
    def make_information(self, data: dict, **kwargs):
        return InformationEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise InformationValidationError(description=exc.normalized_messages())
