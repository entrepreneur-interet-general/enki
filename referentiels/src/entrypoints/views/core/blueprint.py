from flask import Blueprint, current_app, make_response, jsonify
from flask_restful import Api

from .resources.health import HealthResource
from ...extensions import api_spec

core_blueprint = Blueprint(name="core", import_name=__name__, url_prefix="/api")
api = Api(core_blueprint)

api.add_resource(HealthResource, "/health", endpoint="health")


@core_blueprint.before_app_first_request
def register_views():
    api_spec.spec.path(view=HealthResource, app=current_app)


hello_page_blueprint = Blueprint('api', __name__, url_prefix="/")


@hello_page_blueprint.route('/', methods=["GET"])
def hello_referentiels():
    response = make_response(jsonify({'message': 'Hello, Referentiels!'}))
    return response
