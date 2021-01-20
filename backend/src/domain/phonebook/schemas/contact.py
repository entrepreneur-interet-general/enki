from uuid import uuid4
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.phonebook.entities.contact import ContactEntity


class ContactValidationError(HTTPException):
    code = 400


class ContactMethodsSchema(Schema):
    __model__ = ContactEntity

    tel = fields.Dict(keys=fields.Str(), values=fields.Str(), required=True)
    email = fields.Str(required=True)
    address = fields.Str(required=False)


class ContactSchema(Schema):
    __model__ = ContactEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    position = fields.Str(required=True)
    group = fields.Str(required=True)
    contact_methods = fields.Nested(ContactMethodsSchema, required=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    @post_load
    def make_contact(self, data: dict, **kwargs):
        return ContactEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ContactValidationError(description=exc.normalized_messages())
