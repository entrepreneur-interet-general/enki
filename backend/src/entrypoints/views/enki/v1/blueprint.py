from flask import Blueprint, current_app
from flask_restful import Api

from entrypoints.extensions import api_spec, repositories
from .resources import AffairListResource, AffairRandomResource, AffairRandomListResource, \
    TaskListResource, TaskResource, TaskTagResource,TaskTagListResource, \
    TagResource, TagListResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)
# Affairs
api.add_resource(AffairListResource, '/affairs', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affairs")
api.add_resource(AffairRandomResource, '/affair/random', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affair_random")
api.add_resource(AffairRandomListResource, '/affairs/random', resource_class_kwargs={'affairRepo': repositories.affairs}, endpoint="affairs_random")

# Tasks
api.add_resource(TaskListResource, '/tasks', resource_class_kwargs={'task_repo': repositories.task}, endpoint="tasks")
api.add_resource(TaskResource, '/tasks/<uuid>', resource_class_kwargs={'task_repo': repositories.task}, endpoint="task_by_id")
api.add_resource(TaskTagResource, '/tasks/<uuid>/tags/<tag_uuid>', resource_class_kwargs={'task_repo': repositories.task}, endpoint="task_by_id_tag_by_id")
api.add_resource(TaskTagListResource, '/tasks/<uuid>/tags', resource_class_kwargs={'task_repo': repositories.task}, endpoint="task_by_id_tags")

# Tags
api.add_resource(TagListResource, '/tags', resource_class_kwargs={'tag_repo': repositories.tag}, endpoint="tags")
api.add_resource(TagResource, '/tags/<uuid>', resource_class_kwargs={'tag_repo': repositories.tag}, endpoint="tag_by_id")


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
