from flask import Blueprint, current_app

referentiels_blueprint = Blueprint(name="echanges", import_name=__name__, url_prefix="/api")
api = Api(referentiels_blueprint)

api.add_resource(EchangeMessageResource, "/v1/maires", endpoint="maires")


@referentiels_blueprint.before_app_first_request
def register_views():
    api_spec.spec.path(view=EchangeMessageResource, app=current_app)
