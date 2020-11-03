from flask import Blueprint, current_app
from flask_restful import Api

from entrypoints.extensions import api_spec
from .resources import AffairListResource, AffairRandomResource, AffairRandomListResource, \
    TaskListResource, TaskResource, TaskTagResource,TaskTagListResource, \
    TagResource, TagListResource, AffairResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)
# Affairs
api.add_resource(AffairResource, '/affairs/<uuid>', endpoint="affair_by_id")
api.add_resource(AffairListResource, '/affairs', endpoint="affairs")
api.add_resource(AffairRandomResource, '/affair/random',  endpoint="affair_random")
api.add_resource(AffairRandomListResource, '/affairs/random', endpoint="affairs_random")

# Tasks
api.add_resource(TaskListResource, '/tasks', endpoint="tasks")
api.add_resource(TaskResource, '/tasks/<uuid>', endpoint="task_by_id")
api.add_resource(TaskTagResource, '/tasks/<uuid>/tags/<tag_uuid>', endpoint="task_by_id_tag_by_id")
api.add_resource(TaskTagListResource, '/tasks/<uuid>/tags', endpoint="task_by_id_tags")

# Tags
api.add_resource(TagListResource, '/tags', endpoint="tags")
api.add_resource(TagResource, '/tags/<uuid>', endpoint="tag_by_id")


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    # api_spec.spec.components.schema("AffairSchema", schema=AffairSchema)
    api_spec.spec.path(view=AffairListResource, app=current_app)
    api_spec.spec.path(view=AffairRandomResource, app=current_app)
    api_spec.spec.path(view=AffairRandomListResource, app=current_app)

    api_spec.spec.path(view=TaskListResource, app=current_app)
    api_spec.spec.path(view=TaskResource, app=current_app)
    api_spec.spec.path(view=TaskTagResource, app=current_app)
    api_spec.spec.path(view=TaskTagListResource, app=current_app)

    api_spec.spec.path(view=TagListResource, app=current_app)
    api_spec.spec.path(view=TagResource, app=current_app)
