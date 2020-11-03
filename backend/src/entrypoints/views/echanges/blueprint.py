from flask import Blueprint, current_app, make_response, jsonify
from flask_restful import Api

from .resources.echanges import EchangeMessageResource
from ...extensions import api_spec

echanges_blueprint = Blueprint(name="echanges", import_name=__name__, url_prefix="/api")
api = Api(echanges_blueprint)

api.add_resource(EchangeMessageResource, "/v1/echanges/messages", endpoint="echanges_messages")


@echanges_blueprint.before_app_first_request
def register_views():
    api_spec.spec.path(view=EchangeMessageResource, app=current_app)
