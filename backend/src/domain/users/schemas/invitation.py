from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields, post_load, validates_schema
from werkzeug.exceptions import HTTPException

from domain.users.entities.invitation import InvitationEntity
from domain.users.schemas.user import UserSchema


class InvitationValidationError(HTTPException):
    code = 400


class InvitationSchema(Schema):
    __model__ = InvitationEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    token = fields.Str(dump_only=True)
    group_id = fields.Str(load_only=True, required=True)
    group_type = fields.Str(load_only=True, required=True)
    email = fields.Email(required=False)
    phone_number = fields.Str(required=False)
    user_id = fields.Str(dump_only=True)
    creator_id = fields.Str()
    creator = fields.Nested(UserSchema, dump_only=True)
    invitation_url = fields.Str(dump_only=True)
    expire_at = fields.DateTime()
    validated_at = fields.DateTime()
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_invitation(self, data: dict, **kwargs):
        return InvitationEntity.from_dict(data)

    @validates_schema
    def validate_requires(self, data, **kwargs):
        if 'phone_number' not in data and 'email' not in data:
            raise InvitationValidationError(description="Phone number or email needs to be filled")

    def handle_error(self, exc, data, **kwargs):
        raise InvitationValidationError(description=exc.normalized_messages())
