from flask import request, current_app
from flask_restful import Resource
from typing import Dict, Any
from domain.tasks.services.information_service import InformationService
from domain.tasks.command import CreateInformation
from entrypoints.extensions import event_bus


class WithInformationRepoResource(Resource):
    def __init__(self):
        pass


class InformationListResource(WithInformationRepoResource):
    """Get all informations
    ---
    get:
      tags:
        - informations
      summary: Get all informations
      responses:
        '200':
          content:
            application/json:
                schema:  InformationSchema
        '404':
          description: Not Found
    post:
      tags:
        - informations
      summary: Add new information
      requestBody:
        content:
          application/json:
            schema:  InformationSchema
      responses:
        '200':
          content:
            application/json:
                { "message": "Success" }
        '409':
          content:
            application/json:
                description:  { "message": "Information already exists" }
    """

    def get(self):
        return {
                   "informations": InformationService.list_informations(current_app.context)
               }, 200

    def post(self):
        body = request.get_json()
        command = CreateInformation(data=body)
        result = event_bus.publish(command, current_app.context)
        return {"message": "Success"}, 201


class InformationResource(WithInformationRepoResource):
    """Get specific information
    ---
    get:
      tags:
        - informations
      summary: Get specific information
      responses:
        '200':
          content:
            application/json:
                schema:  InformationSchema
        '404':
          description: Not Found
    """

    def get(self, uuid: str):
        return {"information": InformationService.get_by_uuid(uuid, current_app.context), "message": "success"}, 200


class InformationTagListResource(WithInformationRepoResource):
    """Get information's tags
    ---
    get:
      tags:
        - informations
        - tags

    """

    def get(self, uuid: str):
        tags = InformationService.list_tags(uuid, uow=current_app.context)
        return {"tags": tags, "message": "success"}, 200


class InformationTagResource(WithInformationRepoResource):
    """Add, Delete and get specific information's tag
    ---
    put:
      tags:
        - informations
        - tags

    put:
      tags:
        - informations
        - tags

    delete:
      tags:
        - informations
        - tags
    """

    def get(self, uuid: str, tag_uuid: str):
        tag: Dict[str, Any] = InformationService.get_information_tag(uuid,
                                                                     tag_uuid=tag_uuid,
                                                                     uow=current_app.context)
        return {"tag": tag, "message": "Success"}, 200

    def put(self, uuid: str, tag_uuid: str):
        InformationService.add_tag_to_information(uuid,
                                                  tag_uuid=tag_uuid,
                                                  uow=current_app.context)
        return {"message": f"tag {tag_uuid} successfully added from information {uuid}"}, 201

    def delete(self, uuid: str, tag_uuid: str):
        InformationService.remove_tag_to_information(uuid,
                                                     tag_uuid=tag_uuid,
                                                     uow=current_app.context)
        return {"message": f"tag {tag_uuid} successfully deleted from information {uuid}"}, 202
