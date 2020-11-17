from flask import current_app, request
from flask_restful import Resource

from domain.affairs.affair_service import list_affairs, get_by_uuid


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
                   "affair": get_by_uuid(uuid, current_app.context.affair),
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
                   "affairs": list_affairs(current_app.context.affair),
               }, 200
