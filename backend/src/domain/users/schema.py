from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load
from datetime import datetime

from werkzeug.exceptions import HTTPException

from domain.users.entity import UserEntity


class UserValidationError(HTTPException):
    code = 400


class UserSchema(Schema):
    __model__ = UserEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    position = fields.Str(required=False)
    company = fields.Str(required=False)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_user(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return UserEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise UserValidationError(description=exc.normalized_messages())


