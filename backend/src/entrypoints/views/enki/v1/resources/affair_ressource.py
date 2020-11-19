from flask import current_app, request
from flask_restful import Resource

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
        return {
                   "affairs": AffairService.list_affairs(current_app.context.affair),
               }, 200
