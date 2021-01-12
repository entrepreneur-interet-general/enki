import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

from flask import request, current_app, Response, send_from_directory
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from domain.messages.command import CreateResource, UploadResourceContent
from domain.messages.services.resource_service import ResourceService
from entrypoints.extensions import event_bus


class WithResourceContentRepoResource(Resource):
    def __init__(self):
        pass


class ResourceContentResource(WithResourceContentRepoResource):
    """Get specific resource content
    ---
    get:
      tags:
        - resources
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Tag id
      responses:
        200:
          description: data
        404:
            description: Resource not found
    """

    def get(self, uuid: str):
        resource = ResourceService.get_by_uuid(uuid, current_app.context)
        resource_content = ResourceService.load_content(resource["object_path"], current_app.context)
        with NamedTemporaryFile("w") as f:
            with open(f.name, 'wb') as file_data:
                for d in resource_content.stream(32 * 1024):
                    file_data.write(d)
            directory, file_name = "/".join(f.name.split("/")[0:-1]), f.name.split("/")[-1]
            return send_from_directory(directory, file_name)

