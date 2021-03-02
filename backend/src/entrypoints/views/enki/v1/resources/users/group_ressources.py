from flask import request, current_app, g
from flask_restful import Resource, reqparse

from domain.users.entities.group import GroupType
from domain.users.services.group_service import GroupService


class WithGroupRepoResource(Resource):
    def __init__(self):
        pass


class GroupListResource(WithGroupRepoResource):
    """Get all groups with group_type and query
    ---
    get:
      tags:
        - groups
      security:
        - jwt: []
      parameters:
        - in: query
          name: groupType
          required: true
          enum:
            - mairie
            - prefecture
            - partenaire
            - sdis
            - coz
            - cogic
          schema:
            type: str
          description: Type Of groups
        - in: query
          required: true
          name: query
          schema:
            type: str
          description: query to find location
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
        parser = reqparse.RequestParser()
        parser.add_argument('groupType', type=str, required=True, choices=[e.value for e in GroupType])
        parser.add_argument('query', type=str, required=True)

        args = parser.parse_args()
        group_type: str = args.get("groupType")
        query: str = args.get("query")
        return {
                   "data": GroupService.list_groups_from_type_and_query(uow=current_app.context,
                                                                        group_type=group_type,
                                                                        query=query),
                   "message": "success",
               }, 200


class GroupTypeListResource(WithGroupRepoResource):


    def get(self):
        return {
                   "data": GroupService.list_group_types(current_app.context),
                   "message": "success",
               }, 200


class PositionGroupTypeListResource(WithGroupRepoResource):
    """Get all groups
    ---
    get:
      tags:
        - groups
      security:
        - jwt: []
      parameters:
        - in: query
          name: groupType
          required: true
          enum:
            - mairie
            - prefecture
            - partenaire
            - sdis
            - coz
            - cogic
          schema:
            type: str
          description: Type Of groups
      responses:
        200:
          description: Return a list of possible positions
          content:
            application/json:
              schema:
                type: array
                items: PositionSchema
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('groupType', type=str, required=True, choices=[e.value for e in GroupType])

        args = parser.parse_args()
        group_type: str = args.get("groupType")

        return {
                   "data": GroupService.list_positions_by_group_types(group_type=group_type, uow=current_app.context),
                   "message": "success",
               }, 200


class LocationListResource(WithGroupRepoResource):
    """Get all groups
    ---
    get:
      tags:
        - groups
      security:
        - jwt: []
      parameters:
        - in: query
          required: true

          name: query
          schema:
            type: str
          description: query to find location
      responses:
        200:
          description: Return a list of groups
          content:
            application/json:
              schema:
                type: array
                items: LocationSchema
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True)

        args = parser.parse_args()
        query: str = args.get("query")

        return {
                   "data": GroupService.list_location_by_query(query=query, uow=current_app.context),
                   "message": "success",
               }, 200
