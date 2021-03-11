from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load
from werkzeug.exceptions import HTTPException

from domain.evenements.entities.meeting_entity import MeetingEntity


class MessageValidationError(HTTPException):
    code = 400
    description = "Failed to load message"


class MeetingSchema(Schema):
    __model__ = MeetingEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    evenement_id = fields.Str(required=True)
    evenement = fields.Nested("EvenementSchema", dump_only=True)
    link = fields.Str(required=False, dump_only=True)
    creator_id = fields.Str(required=True)
    creator = fields.Nested("UserSchema", dump_only=True)
    participants = fields.Nested("UserSchema", many=True, dump_only=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    closed_at = fields.DateTime(dump_only=True)

    @post_load
    def make_meeting(self, data: dict, **kwargs):
        return MeetingEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise MessageValidationError(description=exc.normalized_messages())
