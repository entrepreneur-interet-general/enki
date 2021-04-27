from __future__ import annotations
from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load
from domain.evenements.entities.reaction_entity import ReactionEntity


class ReactionSchema(Schema):
    __model__ = ReactionEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    type = fields.Str(dump_only=True)
    creator_id = fields.Str(required=False)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_reaction(self, data: dict, **kwargs):
        return ReactionEntity.from_dict(data)
