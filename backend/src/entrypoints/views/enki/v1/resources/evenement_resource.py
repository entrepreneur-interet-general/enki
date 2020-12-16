from datetime import datetime

from flask import request, current_app
from flask_restful import Resource
from typing import Dict, Any

from domain.evenements.entity import EvenementType
from domain.evenements.schema import EvenementSchema
from domain.evenements.service import EvenementService


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
      parameters:
        - in: body
          schema: EvenementSchema
          required: false
          description: Evenement Data
      tags:
        - evenements
    """

    def get(self):
        return {
                   "evenements": EvenementService.list_evenements(current_app.context.evenement)
               }, 200

    def post(self):
        body = request.get_json()
        EvenementService.add_evenement(data=body,
                                       repo=current_app.context.evenement)
        return {"message": "Success"}, 201


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
        - evenements
      responses:
        200:
          description: Return a list of evenements
          content:
            application/json:
              schema: EvenementSchema
    """

    def get(self, uuid: str):
        return {"evenement": EvenementService.get_by_uuid(uuid, current_app.context.evenement),
                "message": "success"}, 200
