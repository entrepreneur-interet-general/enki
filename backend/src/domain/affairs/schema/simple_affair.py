from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load
from werkzeug.exceptions import HTTPException

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.schemas.evenement_schema import EvenementSchema


class AffairValidationError(HTTPException):
    code = 400


class SimpleAffairSchema(Schema):
    __model__ = SimpleAffairEntity
    uuid = fields.Str(missing=lambda: str(uuid4()))
    sge_hub_id = fields.Str(dump_only=True)
    evenement_id = fields.Str(dump_only=True)
    evenement = fields.Nested(EvenementSchema, dump_only=True)
    affair = fields.Dict(dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_simple_affair(self, data: dict, **kwargs):
        return SimpleAffairEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise AffairValidationError(description=exc.normalized_messages())
