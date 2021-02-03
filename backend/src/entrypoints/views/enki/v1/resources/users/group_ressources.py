from flask import request, current_app, g
from flask_restful import Resource

from domain.users.services.group_service import GroupService


class WithGroupRepoResource(Resource):
    def __init__(self):
        pass


class GroupListResource(WithGroupRepoResource):
    """Get all groups
    ---
    get:
      tags:
        - groups
      security:
        - jwt: []
      responses:
        200:
          description: Return a list of groups
          content:
            application/json:
              schema:
                type: array
                items: GroupSchema
    """

    def get(self):
        return {
                   "data": GroupService.list_groups(current_app.context),
                   "message": "success",
               }, 200


class GroupTypeListResource(WithGroupRepoResource):
    """Get all groups
    ---
    get:
      tags:
        - groups
      security:
        - jwt: []
      responses:
        200:
          description: Return a list of groups
    """

    def get(self):
        return {
                   "data": GroupService.list_group_types(current_app.context),
                   "message": "success",
               }, 200
