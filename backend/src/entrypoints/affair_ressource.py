from flask import request
from flask_restful import Resource

from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.affairs.affair_service import list_affairs


class WithAffairRepoResource(Resource):
    def __init__(self, affairRepo: AbstractAffairRepository):
        self.affairRepo = affairRepo


class AffairListResource(WithAffairRepoResource):
    def get(self):
        return {
                   "affairs": list_affairs(self.affairRepo),
            "path":str(self.affairRepo.xml_path)

               }, 200
