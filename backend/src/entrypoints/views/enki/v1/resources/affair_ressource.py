from flask import request
from flask_restful import Resource

from domain.affairs.ports.affair_repository import AbstractAffairRepository
from domain.affairs.affair_service import list_affairs
from entrypoints.views.enki.v1.blueprint import enki_v1_blueprint


class WithAffairRepoResource(Resource):
    def __init__(self, affairRepo: AbstractAffairRepository):
        self.affairRepo = affairRepo


@enki_v1_blueprint.route("/affairs")
class AffairListResource(WithAffairRepoResource):
    @enki_v1_blueprint.route("/affairs")
    def get(self):
        return {
                   "affairs": list_affairs(self.affairRepo),
               }, 200
