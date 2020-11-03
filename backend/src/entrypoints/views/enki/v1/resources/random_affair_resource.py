from flask import current_app
from flask_restful import Resource

from adapters.random.random_cisu_repository import RandomCisuRepository
from domain.affairs.affair_service import list_affairs, get_random_affair, get_random_list_affairs


class WithAffairRepoResource(Resource):
    def __init__(self):
        self.random_repo = RandomCisuRepository()


class AffairRandomResource(WithAffairRepoResource):
    """Get random affair
    ---
    get:
      tags:
        - affairs
    """

    def get(self):
        return {
                   "affair": get_random_affair(self.random_repo),
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
                   "affairs": get_random_list_affairs(self.random_repo),
               }, 200
