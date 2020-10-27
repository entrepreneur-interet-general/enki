from flask import request
from flask_restful import Resource

from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.affairs.affair_service import list_affairs, get_random_affair, get_random_list_affairs


class WithAffairRepoResource(Resource):
    def __init__(self, affairRepo: AbstractAffairRepository):
        self.affairRepo = affairRepo


class AffairResource(WithAffairRepoResource):
    """Get random affair
    ---
    get:
      tags:
        - affairs
    """

    def get(self):
        return {
                   "affairs": list_affairs(self.affairRepo),
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
                   "affair": get_random_affair(self.affairRepo),
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
                   "affairs": get_random_list_affairs(self.affairRepo),
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
                   "affairs": list_affairs(self.affairRepo),
               }, 200
