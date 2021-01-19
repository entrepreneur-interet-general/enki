from uuid import uuid4
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.phonebook.entities.contact import ContactEntity


class ContactValidationError(HTTPException):
    code = 400

@dataclass
@dataclass_json
class ContactMethods:
    tel: str
    email: str
    address: str


class ContactSchema(Schema):
    __model__ = ContactEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)
    updated_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)


class ContactMethodsSchema(Schema):
    __model__ = ContactEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    tel = fields.Str(required=True)
    email = fields.Str(required=True)
    address = fields.Str(required=True)




    def _build_download_link(self, obj):
        return f"/api/enki/v1/resources/{obj.uuid}/content"

    @post_load
    def make_resource(self, data: dict, **kwargs):
        return ContactEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ContactValidationError(description=exc.normalized_messages())
