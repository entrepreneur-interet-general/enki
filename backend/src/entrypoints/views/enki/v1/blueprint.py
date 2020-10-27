from flask import Blueprint, current_app
from flask_restful import Api

from entrypoints.extensions import api_spec, repositories
from .resources import AffairListResource, TaskListResource, TaskResource, AffairRandomResource, AffairRandomListResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)
# Affairs
api.add_resource(AffairListResource, '/affairs', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affairs")
api.add_resource(AffairRandomResource, '/affair/random', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affairs")
api.add_resource(AffairRandomListResource, '/affairs/random', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affairs")

# Tasks
api.add_resource(TaskListResource, '/tasks', resource_class_kwargs={'taskRepo': repositories.task}, endpoint="tasks")
api.add_resource(TaskResource, '/tasks/<uuid>', resource_class_kwargs={'taskRepo': repositories.task}, endpoint="task_by_id")


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    # api_spec.spec.components.schema("AffairSchema", schema=AffairSchema)
    api_spec.spec.path(view=AffairListResource, app=current_app)
    api_spec.spec.path(view=TaskListResource, app=current_app)
    api_spec.spec.path(view=TaskResource, app=current_app)
