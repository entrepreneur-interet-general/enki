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
    object_path = fields.Method("_object_path")
    message_id = fields.Str(required=False, dump_only=True)
    original_name = fields.Str(required=False)
    content_type = fields.Str(required=False, validate=validate.OneOf(content_types))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    def _object_path(self, obj):
        return obj.uuid

    def _bucket_name(self, obj):
        return self.context.bucket_name_config

    @post_load
    def make_resource(self, data: dict, **kwargs):
        data["bucket_name"] = self.context["bucket_name_config"]
        data["object_path"] = data["uuid"]
        return ResourceEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ResourceValidationError(description=exc.normalized_messages())
