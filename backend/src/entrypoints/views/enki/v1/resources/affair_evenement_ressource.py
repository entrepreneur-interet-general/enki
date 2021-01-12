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
    get:
      tags:
        - affairs
    """

    def put(self, uuid, evenement_id):
        AffairService.assign_affair_to_evenement(uuid, evenement_id, current_app.context)
        return {"message": f"message {uuid} successfully added to evenement {evenement_id}"}, 201

    def delete(self, uuid, evenement_id):
        AffairService.delete_affair_from_evenement(uuid, evenement_id, current_app.context)
        return {"message": f"message {uuid} successfully deleted to evenement {evenement_id}"}, 201