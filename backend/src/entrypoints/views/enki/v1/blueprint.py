from flask import Blueprint, current_app
from flask_restful import Api

from domain.evenements.schema import EvenementSchema
from domain.tasks.schema import TaskSchema, TagSchema, InformationSchema
from entrypoints.extensions import api_spec
from .resources import AffairListResource, AffairRandomResource, AffairRandomListResource, \
    TaskListResource, TaskResource, TaskTagResource, TaskTagListResource, \
    TagResource, TagListResource, AffairResource, \
    EvenementListResource, EvenementResource, \
    InformationResource, InformationListResource, InformationTagListResource, InformationTagResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)
# Affairs
api.add_resource(AffairResource, '/affairs/<uuid>', endpoint="affair_by_id")
api.add_resource(AffairListResource, '/affairs', endpoint="affairs")
api.add_resource(AffairRandomResource, '/affair/random', endpoint="affair_random")
api.add_resource(AffairRandomListResource, '/affairs/random', endpoint="affairs_random")

# Tasks
api.add_resource(TaskListResource, '/tasks', endpoint="tasks")
api.add_resource(TaskResource, '/tasks/<uuid>', endpoint="task_by_id")
api.add_resource(TaskTagResource, '/tasks/<uuid>/tags/<tag_uuid>', endpoint="task_by_id_tag_by_id")
api.add_resource(TaskTagListResource, '/tasks/<uuid>/tags', endpoint="task_by_id_tags")

# Informations
api.add_resource(InformationListResource, '/informations', endpoint="informations")
api.add_resource(InformationResource, '/informations/<uuid>', endpoint="information_by_id")
api.add_resource(InformationTagResource, '/informations/<uuid>/tags/<tag_uuid>', endpoint="information_by_id_tag_by_id")
api.add_resource(InformationTagListResource, '/informations/<uuid>/tags', endpoint="information_by_id_tags")

# Tags
api.add_resource(TagListResource, '/tags', endpoint="tags")
api.add_resource(TagResource, '/tags/<uuid>', endpoint="tag_by_id")

# Evenements
api.add_resource(EvenementListResource, '/events', endpoint="events")
api.add_resource(EvenementResource, '/events/<uuid>', endpoint="events_by_id")


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    api_spec.spec.components.schema("EvenementSchema", schema=EvenementSchema)
    api_spec.spec.components.schema("TaskSchema", schema=TaskSchema)
    api_spec.spec.components.schema("TagSchema", schema=TagSchema)
    api_spec.spec.components.schema("InformationSchema", schema=InformationSchema)

    # Affairs
    api_spec.spec.path(view=AffairListResource, app=current_app)
    api_spec.spec.path(view=AffairRandomResource, app=current_app)
    api_spec.spec.path(view=AffairRandomListResource, app=current_app)

    # Tags
    api_spec.spec.path(view=TagListResource, app=current_app)
    api_spec.spec.path(view=TagResource, app=current_app)

    # Tasks
    api_spec.spec.path(view=TaskListResource, app=current_app)
    api_spec.spec.path(view=TaskResource, app=current_app)

    # Tag <> Tasks
    api_spec.spec.path(view=TaskTagResource, app=current_app)
    api_spec.spec.path(view=TaskTagListResource, app=current_app)

    # Informations
    api_spec.spec.path(view=InformationListResource, app=current_app)
    api_spec.spec.path(view=InformationResource, app=current_app)

    # Tag <> Informations
    api_spec.spec.path(view=InformationTagListResource, app=current_app)
    api_spec.spec.path(view=InformationTagResource, app=current_app)

    # Evenements
    api_spec.spec.path(view=EvenementListResource, app=current_app)
    api_spec.spec.path(view=EvenementResource, app=current_app)
