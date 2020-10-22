from flask import request
from flask_restful import Resource

from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.affairs.affair_service import list_affairs


class WithAffairRepoResource(Resource):
    def __init__(self, affairRepo: AbstractAffairRepository):
        self.affairRepo = affairRepo


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
