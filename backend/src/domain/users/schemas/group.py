from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime

from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException

from domain.users.entities.group import GroupEntity, GroupType, PositionGroupTypeEntity, LocationEntity, LocationType


class GroupValidationError(HTTPException):
    code = 400


class LocationSchema(Schema):
    __model__ = LocationEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    label = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    external_id = fields.Str(dump_only=True)
    search_label = fields.Str(dump_only=True)
    type = EnumField(LocationType, validate=validate.OneOf([e.value for e in LocationType]))

    @post_load
    def make_location(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return LocationEntity.from_dict(data)

class GroupSchema(Schema):
    __model__ = GroupEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    label = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    type = EnumField(GroupType, validate=validate.OneOf([e.value for e in GroupType]))
    location = fields.Nested(LocationSchema, dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_group(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return GroupEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise GroupValidationError(description=exc.normalized_messages())


class PositionGroupTypeEntitySchema(Schema):
    __model__ = PositionGroupTypeEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    label = fields.Str(required=True)
    slug = fields.Str(dump_only=True)
    group_type = EnumField(GroupType, validate=validate.OneOf([e.value for e in GroupType]))

    @post_load
    def make_position(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return PositionGroupTypeEntity.from_dict(data)

