from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from datetime import datetime

from domain.evenements.entity import EvenementType


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
