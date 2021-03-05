from datetime import datetime

from flask import request, current_app, g
from flask_restful import Resource
from typing import Dict, Any

from domain.evenements.command import CreateEvenement
from domain.evenements.entity import EvenementRoleType
from entrypoints.extensions import event_bus
from domain.evenements.service import EvenementService
from entrypoints.middleware import user_info_middleware


class WithEvenementRepoResource(Resource):
    def __init__(self):
        pass


class EvenementInviteUserResource(WithEvenementRepoResource):
    """Get all evenements
    ---
    put:
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

    def put(self, uuid: str, user_uuid: str):
        result = EvenementService.invite_user(uuid=uuid,
                                              user_id=user_uuid,
                                              role_type=EvenementRoleType.VIEW,
                                              uow=current_app.context)
        return {
                   "message": "success",
                   "data": result,
               }, 201
