from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity, TaskType


class TaskValidationError(HTTPException):
    code = 400


class TagValidationError(HTTPException):
    code = 400


class TaskSchema(Schema):
    __model__ = TaskEntity

    uuid = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    type = EnumField(TaskType, by_value=True)
    event_type = fields.Str(default="task")
    executor_id = fields.Str(required=False)
    executor_type = fields.Str(required=False)
    done_atv= fields.DateTime(default=datetime.utcnow())
    created_at = fields.DateTime(default=datetime.utcnow())
    updated_at = fields.DateTime(default=datetime.utcnow())

    @post_load
    def make_task(self, data: dict, **kwargs):
        return TaskEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise TaskValidationError(description=exc.normalized_messages())


class TagSchema(Schema):
    __model__ = TagEntity

    uuid = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    event_type = fields.Str(required=False)
    creator_id = fields.Str(required=False)
    created_at = fields.DateTime(default=datetime.utcnow())
    updated_at = fields.DateTime(default=datetime.utcnow())

    @post_load
    def make_tag(self, data: dict, **kwargs):
        return TagEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise TagValidationError(description=exc.normalized_messages())




