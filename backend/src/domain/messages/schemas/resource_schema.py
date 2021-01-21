from uuid import uuid4
from marshmallow import Schema, fields, post_load, validate
from datetime import datetime
from werkzeug.exceptions import HTTPException

from domain.messages.entities.resource import ResourceEntity, content_types
from entrypoints.extensions import minio


class ResourceValidationError(HTTPException):
    code = 400


class ResourceSchema(Schema):
    __model__ = ResourceEntity

    uuid = fields.Str(missing=lambda: str(uuid4()))
    creator_id = fields.Str(required=False, dump_only=True)
    bucket_name = fields.Str(required=False, dump_only=True)
    object_path = fields.Method("_object_path")
    url = fields.Method("_build_get_presigned_url")
    upload_url = fields.Method("_build_update_presigned_url")
    message_id = fields.Str(required=False, dump_only=True)
    original_name = fields.Str(required=False)
    content_type = fields.Str(required=False, validate=validate.OneOf(content_types))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow(), dump_only=True)

    def _object_path(self, obj):
        return obj.uuid

    def _bucket_name(self, obj):
        return self.context.bucket_name_config

    def _build_get_presigned_url(self, obj):
        return minio.get_presigned_get_url(bucket=obj.bucket_name, object_path=obj.object_path)

    def _build_update_presigned_url(self, obj):
        return minio.get_presigned_put_url(bucket=obj.bucket_name, object_path=obj.object_path)

    @post_load
    def make_resource(self, data: dict, **kwargs):
        data["bucket_name"] = self.context["bucket_name_config"]
        data["object_path"] = data["uuid"]
        return ResourceEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ResourceValidationError(description=exc.normalized_messages())
