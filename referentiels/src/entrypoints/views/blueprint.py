from flask import Blueprint, current_app
from flask_restful import Api
from ..extensions import api_spec
from .resources.elus.maire import MairesResource

referentiels_blueprint = Blueprint(name="referentiels", import_name=__name__, url_prefix="/api")
api = Api(referentiels_blueprint)

api.add_resource(MairesResource, "/v1/maires", endpoint="maires")


@referentiels_blueprint.before_app_first_request
def register_views():
    api_spec.spec.path(view=MairesResource, app=current_app)
