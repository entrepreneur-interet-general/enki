from flask import current_app
from flask_restful import Resource

from domain.affairs.affair_service import list_affairs, get_random_affair, get_random_list_affairs


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

    def get(self):
        return {
                   "affairs": list_affairs(current_app.context.affair),
               }, 200


class AffairRandomResource(WithAffairRepoResource):
    """Get random affair
    ---
    get:
      tags:
        - affairs
    """

    def get(self):
        return {
                   "affair": get_random_affair(current_app.context.affair),
               }, 200


class AffairRandomListResource(WithAffairRepoResource):
    """Get random affair
        ---
        get:
          tags:
            - affairs
        """

    def get(self):
        return {
                   "affairs": get_random_list_affairs(current_app.context.affair),
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
