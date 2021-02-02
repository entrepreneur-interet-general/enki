from flask import current_app, request
from flask_restful import Resource, reqparse
from typing import Union, List

from domain.affairs.services.affair_service import AffairService


class WithAffairRepoResource(Resource):
    def __init__(self):
        pass


class AffairResource(WithAffairRepoResource):
    """Get random affair
    ---
    get:
      tags:
        - affairs
    """

    def get(self, uuid):
        return {
                   "data": AffairService.get_by_uuid(uuid, current_app.context),
                   "message": "success"
               }, 200


class AffairListResource(WithAffairRepoResource):
    """All affairs list

    ---
    get:
        description: Getting all current french mayors
        parameters:
          - in: query
            name: insee_code
            schema:
              type: string
            required: false
            description: City code
          - in: query
            name: postal_code
            schema:
              type: string
            required: false
            description: Postal code
          - in: query
            name: dept_code
            schema:
              type: string
            required: false
            description: Postal code
        tags:
          - affairs
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('insee_code', type=str, help='Insee code', action='append')
        parser.add_argument('postal_code', type=str, help='Postal code', action='append')
        parser.add_argument('dept_code', type=str, help='Departement code', action='append')
        args = parser.parse_args()

        postal_codes: Union[str, List[str], None] = args.get("postal_code")
        insee_code: Union[str, List[str], None] = args.get("insee_code")
        dept_code: Union[str, List[str], None] = args.get("dept_code")

        if postal_codes or insee_code:
            affairs = AffairService.list_affairs_by_insee_and_postal_codes(insee_code=insee_code,
                                                                           postal_code=postal_codes,
                                                                           dept_code=dept_code,
                                                                           uow=current_app.context)
        else:
            affairs = AffairService.list_affairs(uow=current_app.context)

        return {
                   "data": affairs,
                   "message": "success"
               }, 200
