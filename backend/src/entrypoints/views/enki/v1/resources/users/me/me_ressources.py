from flask import current_app, g
from flask_restful import Resource

from domain.users.services.user_service import UserService
from entrypoints.middleware import user_info_middleware


class WithUserRepoResource(Resource):
    def __init__(self):
        pass


class UserMeResource(WithUserRepoResource):
    """Get specific user
    ---
    get:
      tags:
        - me
        - user
      responses:
        200:
          description: Return my specific user
          content:
            application/json:
              schema: UserSchema
        404:
            description: User not found
    """
    method_decorators = [user_info_middleware]

    def get(self):
        return {
                   "data": UserService.get_by_uuid(uuid=g.user_info["id"], uow=current_app.context),
                   "message": "success"
               }, 200
