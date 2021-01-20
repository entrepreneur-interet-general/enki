from uuid import uuid4
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.messages.entities.resource import ResourceEntity, content_types


class ResourceValidationError(HTTPException):
    code = 400


class ResourceSchema(Schema):
    __model__ = ResourceEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    creator_id = fields.Str(required=False, dump_only=True)
    bucket_name = fields.Str(required=False, dump_only=True)
    object_path = fields.Str(required=False, dump_only=True)
    message_id = fields.Str(required=False, dump_only=True)
    original_name = fields.Str(required=False)
    content_type = fields.Str(required=False, validate=validate.OneOf(content_types.keys()))
    extensions = fields.Str(required=False, validate=validate.OneOf(content_types.values()))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    def _bucket_name(self, obj):
        return self.context.bucket_name_config

    @post_load
    def make_resource(self, data: dict, **kwargs):
        data["bucket_name"] = self.context["bucket_name_config"]
        data["extension"] = data["original_name"].split(".")[-1]
        data["object_path"] = f'{data["uuid"]}.{data["extension"]}'
        return ResourceEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ResourceValidationError(description=exc.normalized_messages())
