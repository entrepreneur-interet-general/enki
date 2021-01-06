from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
from datetime import datetime
from marshmallow.exceptions import ValidationError

from werkzeug.exceptions import HTTPException

from domain.evenements.entity import EvenementType, EvenementEntity


class EvenementValidationError(HTTPException):
    code = 400


class EvenementSchema(Schema):
    __model__ = EvenementEntity

    uuid = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    type = EnumField(EvenementType, required=True, by_value=True)
    creator_id = fields.Str(required=False)
    started_at = fields.DateTime(required=True)
    ended_at = fields.DateTime(required=False)
    created_at = fields.DateTime(default=datetime.utcnow())
    updated_at = fields.DateTime(default=datetime.utcnow())

    @post_load
    def make_event(self, data: dict, **kwargs):
        return EvenementEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise EvenementValidationError(description=exc.normalized_messages())


