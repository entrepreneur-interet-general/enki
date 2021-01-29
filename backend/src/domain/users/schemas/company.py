from uuid import uuid4

from flask import current_app
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime

from marshmallow_enum import EnumField
from werkzeug.exceptions import HTTPException

from domain.users.entities.company import CompanyEntity, CompanyType


class CompanyValidationError(HTTPException):
    code = 400


class CompanySchema(Schema):
    __model__ = CompanyEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    name = fields.Str(required=True)
    type = EnumField(CompanyType, validate=validate.OneOf([e.value for e in CompanyType]))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())

    @post_load
    def make_company(self, data: dict, **kwargs):
        current_app.logger.info(f"data {data}")
        return CompanyEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise CompanyValidationError(description=exc.normalized_messages())


