from flask import Blueprint, current_app
from flask_restful import Api
from ..extensions import api_spec
from .resources.elus.maire import MairesResource
from .resources.municipality import MunicipalitiesTextualSearchResource
referentiels_blueprint = Blueprint(name="referentiels", import_name=__name__, url_prefix="/api")
api = Api(referentiels_blueprint)

api.add_resource(MairesResource, "/v1/maires", endpoint="maires")
api.add_resource(MunicipalitiesTextualSearchResource, "/v1/municipality", endpoint="municipality_textual_search")


@referentiels_blueprint.before_app_first_request
def register_views():
    api_spec.spec.path(view=MairesResource, app=current_app)
    api_spec.spec.path(view=MunicipalitiesTextualSearchResource, app=current_app)
