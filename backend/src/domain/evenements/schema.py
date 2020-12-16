from marshmallow import Schema, fields,  post_load
from marshmallow_enum import EnumField
from datetime import datetime

from domain.evenements.entity import EvenementType, EvenementEntity


class EvenementSchema(Schema):
    uuid = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    type = EnumField(EvenementType)
    creator_id = fields.Str(required=False)
    started_at = fields.DateTime(required=True)
    ended_at = fields.DateTime(required=False)
    created_at = fields.DateTime(default=datetime.now())
    updated_at = fields.DateTime(default=datetime.now())

    @post_load
    def make_event(self, data: dict, **kwargs):
        return EvenementEntity.from_dict(data)
