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
    creator_id = fields.Str(required=False)
    bucket_name = fields.Str(required=False)
    object_path = fields.Str(required=False)
    message_id = fields.Str(required=False)
    original_name = fields.Str(required=False)
    content_type = fields.Str(required=False, validate=validate.OneOf(content_types))
    created_at = fields.DateTime(missing=lambda: datetime.utcnow())
    path_to_download = fields.Method("_build_download_link")

    def _build_download_link(self, obj):
        return f"/api/enki/v1/resources/{obj.uuid}/content"

    @post_load
    def make_resource(self, data: dict, **kwargs):
        return ResourceEntity.from_dict(data)

    def handle_error(self, exc, data, **kwargs):
        raise ResourceValidationError(description=exc.normalized_messages())
