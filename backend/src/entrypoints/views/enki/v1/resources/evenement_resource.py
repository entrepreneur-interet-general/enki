from datetime import datetime

from flask import request, current_app, g
from flask_restful import Resource
from typing import Dict, Any

from domain.evenements.command import CreateEvenement
from entrypoints.extensions import event_bus
from domain.evenements.service import EvenementService
from entrypoints.middleware import user_info_middleware


class WithEvenementRepoResource(Resource):
    def __init__(self):
        pass


class EvenementListResource(WithEvenementRepoResource):
    """Get all evenements
    ---
    get:
      tags:
        - evenements
      responses:
        200:
          description: Return a list of evenements
          content:
            application/json:
              schema:
                type: array
                items: EvenementSchema
    post:
      description: Creating an event
      tags:
        - events
      requestBody:
        content:
          application/json:
            schema:  EvenementSchema
      responses:
        201:
          description: Successfully created
        400:
          description: bad request, bad parameters
    """
    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": EvenementService.list_evenements(current_app.context),
                   "message": "success",
               }, 200

    def post(self):
        body = request.get_json()
        body["creator_id"] = g.user_info["id"]
        command = CreateEvenement(data=body)
        result = event_bus.publish(command, current_app.context)

        return {
                   "message": "success",
                   "data": result[0],
               }, 201


class EvenementResource(WithEvenementRepoResource):
    """Get specific evenement
    ---
    get:
      parameters:
        - in: path
          name: uuid
          schema:
            type: string
          required: true
          description: Event id
      tags:
        - events
      responses:
        200:
          description: Return a list of evenements
          content:
            application/json:
              schema: EvenementSchema
    """

    def get(self, uuid: str):
        return {
                   "data": EvenementService.get_by_uuid(uuid, current_app.context),
                   "message": "success",
               }, 200
