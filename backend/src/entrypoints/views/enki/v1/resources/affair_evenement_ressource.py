from flask import current_app, request
from flask_restful import Resource, reqparse
from typing import Union, List

from domain.affairs.services.affair_service import AffairService


class WithAffairEvenementRepoResource(Resource):
    def __init__(self):
        pass


class AffairEvenementResource(WithAffairEvenementRepoResource):
    """Get random affair
    ---
    put:
      tags:
        - evenement <> affairs
    delete:
      tags:
        - evenement <> affairs
    """

    def put(self, uuid, affair_id):
        AffairService.assign_affair_from_evenement(affair_id, uuid, current_app.context)
        return {"message": f"affair {affair_id} successfully added to evenement {uuid}"}, 201

    def delete(self, uuid, affair_id):
        AffairService.delete_affair_from_evenement(affair_id, uuid, current_app.context)
        return {"message": f"affair {uuid} successfully deleted to evenement {uuid}"}, 201


class AffairListEvenementResource(WithAffairEvenementRepoResource):
    """Get random affair
    ---
    get:
      tags:
        - evenement <> affairs
    """

    def get(self, uuid):
        affairs = AffairService.list_affairs_by_evenement(uuid, current_app.context)
        return {"data": affairs,
                "message": "success"}, 201
