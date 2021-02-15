from flask import current_app, g
from flask_restful import Resource

from domain.users.services.user_service import UserService
from entrypoints.middleware import user_info_middleware


class WithUserRepoResource(Resource):
    def __init__(self):
        pass


class UserMeAffairsResource(WithUserRepoResource):
    """Get specific user
    ---
    get:
      tags:
        - me
        - affairs
      responses:
        200:
          description: Return my specific user
        404:
            description: User not found
    """
    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": UserService.get_affairs_by_user_uuid(uuid=g.user_info["id"], uow=current_app.context),
                   "message": "success"
               }, 200
