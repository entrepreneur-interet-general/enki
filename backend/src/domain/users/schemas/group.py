from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime

from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException

from domain.users.entities.group import GroupEntity, GroupType


class GroupValidationError(HTTPException):
    code = 400


class GroupSchema(Schema):
    __model__ = GroupEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    name = fields.Str(required=True)
    type = EnumField(GroupType, validate=validate.OneOf([e.value for e in GroupType]))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_group(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return GroupEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise GroupValidationError(description=exc.normalized_messages())


