from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from datetime import datetime

from werkzeug.exceptions import HTTPException

from domain.evenements.entity import EvenementType, EvenementEntity


class EvenementValidationError(HTTPException):
    code = 400


class EvenementSchema(Schema):
    __model__ = EvenementEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    title = fields.Str(required=True, validate=validate.Length(min=5, max=255))
    description = fields.Str(required=True, validate=validate.Length(min=5, max=1000))
    type = EnumField(EvenementType, required=True, by_value=True)
    started_at = fields.DateTime(required=True)
    creator_id = fields.Str(required=False)
    ended_at = fields.DateTime(required=False)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_event(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return EvenementEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise EvenementValidationError(description=exc.normalized_messages())


