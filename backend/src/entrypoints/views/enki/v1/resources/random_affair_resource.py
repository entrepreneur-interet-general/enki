from flask import current_app
from flask_restful import Resource

from adapters.random.random_cisu_repository import RandomCisuRepository
from domain.affairs.services.affair_service import AffairService


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
                   "affair": AffairService.get_random_affair(self.random_repo),
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
                   "affairs": AffairService.get_random_list_affairs(self.random_repo),
               }, 200
