from flask import Blueprint, current_app
from flask_restful import Api

from domain.evenements.schema import EvenementSchema
from domain.messages.schemas.schema import MessageSchema
from entrypoints.extensions import api_spec
from .resources import AffairListResource, AffairRandomResource, AffairRandomListResource, \
    MessageListResource, MessageResource, \
    MessageTagResource, MessageTagListResource, \
    TagResource, TagListResource, AffairResource, \
    EvenementListResource, EvenementResource, \
    ResourceListResource, ResourceResource, \
    MessageResourceResource, MessageResourceListResource, \
    ResourceContentResource

enki_blueprint_v1 = Blueprint(name="enki_blueprint_v1", import_name=__name__, url_prefix="/api/enki/v1")

api = Api(enki_blueprint_v1)
# Affairs
api.add_resource(AffairResource, '/affairs/<uuid>', endpoint="affair_by_id")
api.add_resource(AffairListResource, '/affairs', endpoint="affairs")
api.add_resource(AffairRandomResource, '/affair/random', endpoint="affair_random")
api.add_resource(AffairRandomListResource, '/affairs/random', endpoint="affairs_random")

# Messages
api.add_resource(MessageListResource, '/messages', endpoint="messages")
api.add_resource(MessageResource, '/messages/<uuid>', endpoint="message_by_id")

# Tags
api.add_resource(TagListResource, '/tags', endpoint="tags")
api.add_resource(TagResource, '/tags/<uuid>', endpoint="tag_by_id")
api.add_resource(MessageTagResource, '/messages/<uuid>/tags/<tag_uuid>', endpoint="message_by_id_tag_by_id")
api.add_resource(MessageTagListResource, '/messages/<uuid>/tags', endpoint="message_by_id_tags")

# Resources
api.add_resource(ResourceListResource, '/resources', endpoint="resources")
api.add_resource(ResourceResource, '/resources/<uuid>', endpoint="resource_by_id")
api.add_resource(ResourceContentResource, '/resources/<uuid>/content', endpoint="resource_by_id_content")
api.add_resource(MessageResourceResource, '/messages/<uuid>/resource/<tag_uuid>', endpoint="message_by_id_resource_by_id")
api.add_resource(MessageResourceListResource, '/messages/<uuid>/resources', endpoint="message_by_id_resources")

# Evenements
api.add_resource(EvenementListResource, '/events', endpoint="events")
api.add_resource(EvenementResource, '/events/<uuid>', endpoint="events_by_id")


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    api_spec.spec.components.schema("EvenementSchema", schema=EvenementSchema)
    api_spec.spec.components.schema("MessageSchema", schema=MessageSchema)
    #api_spec.spec.components.schema("TagSchema", schema=TagSchema)

    # Affairs
    api_spec.spec.path(view=AffairListResource, app=current_app)
    api_spec.spec.path(view=AffairRandomResource, app=current_app)
    api_spec.spec.path(view=AffairRandomListResource, app=current_app)

    # Messages
    api_spec.spec.path(view=MessageListResource, app=current_app)
    api_spec.spec.path(view=MessageResource, app=current_app)

    # Tags
    api_spec.spec.path(view=TagListResource, app=current_app)
    api_spec.spec.path(view=TagResource, app=current_app)

    # Tag <> Messages
    api_spec.spec.path(view=MessageTagResource, app=current_app)
    api_spec.spec.path(view=MessageTagListResource, app=current_app)

    # Resources
    api_spec.spec.path(view=ResourceResource, app=current_app)
    api_spec.spec.path(view=ResourceListResource, app=current_app)
    api_spec.spec.path(view=ResourceContentResource, app=current_app)

    # Resource <> Messages
    api_spec.spec.path(view=MessageResourceResource, app=current_app)
    api_spec.spec.path(view=MessageResourceListResource, app=current_app)

    # Evenements
    api_spec.spec.path(view=EvenementListResource, app=current_app)
    api_spec.spec.path(view=EvenementResource, app=current_app)
