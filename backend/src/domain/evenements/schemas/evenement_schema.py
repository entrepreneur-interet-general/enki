from datetime import datetime
from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException

from domain.evenements.entities.evenement_entity import EvenementType, EvenementEntity
from domain.users.schemas.user import UserSchema


class EvenementValidationError(HTTPException):
    code = 400


class EvenementSchema(Schema):
    __model__ = EvenementEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    type = EnumField(EvenementType, required=True, by_value=True)
    started_at = fields.DateTime(required=True)
    closed = fields.Boolean(dump_only=True)
    creator_id = fields.Str(required=False, dump_only=True)
    creator = fields.Nested(UserSchema, required=False, dump_only=True)
    ended_at = fields.DateTime(required=False, dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_event(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return EvenementEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise EvenementValidationError(description=exc.normalized_messages())


