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
                   "affair": AffairService.get_by_uuid(uuid, current_app.context.affair),
               }, 200


class AffairListResource(WithAffairRepoResource):
    """All affairs list
    ---
    get:
      tags:
        - affairs
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('insee_code', type=str, help='Insee code')
        parser.add_argument('postal_code', type=str, help='Postal code')
        args = parser.parse_args()

        postal_codes: Union[str, List[str], None] = args.get("postal_code")
        insee_code: Union[str, List[str], None] = args.get("insee_code")

        if postal_codes or insee_code:
            affairs = AffairService.list_affairs_by_insee_and_postal_codes(insee_code=insee_code,
                                                                           postal_code=postal_codes,
                                                                           repo=current_app.context.affair)
        else:
            affairs = AffairService.list_affairs(repo=current_app.context.affair)

        return {"affairs": affairs}, 200
