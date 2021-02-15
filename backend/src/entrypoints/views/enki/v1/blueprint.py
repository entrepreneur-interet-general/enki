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
    AffairEvenementResource, AffairListEvenementResource
from .resources.contact_ressources import ContactListResource, ContactResource
from entrypoints.views.enki.v1.resources.users.user_ressources import UserResource, UserListResource
from .resources.message_resource_resource import MessageMultipleResourceResource
from .resources.users.group_ressources import GroupListResource, GroupTypeListResource, LocationListResource, \
    PositionGroupTypeListResource
from .resources.users.me.me_affairs_ressources import UserMeAffairsResource
from .resources.users.me.me_ressources import UserMeResource
from .resources.users.user_favorite_ressources import UserContactListResource, UserContactResource

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

api.add_resource(MessageResourceResource, '/messages/<uuid>/resource/<resource_uuid>',
                 endpoint="message_by_id_resource_by_id")
api.add_resource(MessageMultipleResourceResource, '/messages/<uuid>/resource/add',
                 endpoint="message_by_id_resource_by_ids")


api.add_resource(MessageResourceListResource, '/messages/<uuid>/resources', endpoint="message_by_id_resources")

# Evenements
api.add_resource(EvenementListResource, '/events', endpoint="events")
api.add_resource(EvenementResource, '/events/<uuid>', endpoint="events_by_id")

# Affairs <> Evenement
api.add_resource(AffairEvenementResource, '/events/<uuid>/affairs/<affair_uuid>', endpoint="evenement_affairs_by_id")
api.add_resource(AffairListEvenementResource, '/events/<uuid>/affairs', endpoint="evenement_affairs_list")

# User
api.add_resource(UserListResource, '/users', endpoint="users")
api.add_resource(UserResource, '/users/<uuid>', endpoint="users_by_id")

# User
api.add_resource(ContactListResource, '/contacts', endpoint="contacts")
api.add_resource(ContactResource, '/contacts/<uuid>', endpoint="contacts_by_id")

# Groups
api.add_resource(GroupListResource, '/groups', endpoint="groups")
api.add_resource(GroupTypeListResource, '/groups/types', endpoint="groups_types")
api.add_resource(PositionGroupTypeListResource, '/groups/positions', endpoint="groups_type_positions")
api.add_resource(LocationListResource, '/groups/locations', endpoint="groups_locations")

# User <> Contacts
api.add_resource(UserContactListResource, '/users/me/contact/favorites', endpoint="user_contacts")
api.add_resource(UserContactResource, '/users/me/contact/favorites/<contact_uuid>', endpoint="user_contacts_by_id")

# Me
api.add_resource(UserMeResource, '/users/me', endpoint="me_informations")
api.add_resource(UserMeAffairsResource, '/users/me/affairs', endpoint="me_affairs")


@enki_blueprint_v1.before_app_first_request
def register_views():
    # Add documents Schemas
    api_spec.spec.components.schema("EvenementSchema", schema=EvenementSchema)
    api_spec.spec.components.schema("MessageSchema", schema=MessageSchema)
    api_spec.spec.components.schema("UserSchema", schema=MessageSchema)
    # api_spec.spec.components.schema("TagSchema", schema=TagSchema)

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
    api_spec.spec.path(view=MessageMultipleResourceResource, app=current_app)
    api_spec.spec.path(view=ResourceListResource, app=current_app)

    # Resource <> Messages
    api_spec.spec.path(view=MessageResourceResource, app=current_app)
    api_spec.spec.path(view=MessageResourceListResource, app=current_app)

    # Evenements
    api_spec.spec.path(view=EvenementListResource, app=current_app)
    api_spec.spec.path(view=EvenementResource, app=current_app)

    # Affairs <> Evenement
    api_spec.spec.path(view=AffairEvenementResource, app=current_app)
    api_spec.spec.path(view=AffairListEvenementResource, app=current_app)

    # Users
    api_spec.spec.path(view=UserListResource, app=current_app)
    api_spec.spec.path(view=UserResource, app=current_app)

    # Groups
    api_spec.spec.path(view=GroupListResource, app=current_app)
    api_spec.spec.path(view=GroupTypeListResource, app=current_app)
    # Groups Locations & positions
    api_spec.spec.path(view=PositionGroupTypeListResource, app=current_app)
    api_spec.spec.path(view=LocationListResource, app=current_app)

    # Contacts
    api_spec.spec.path(view=ContactListResource, app=current_app)
    api_spec.spec.path(view=ContactResource, app=current_app)

    # Users <> Contacts
    api_spec.spec.path(view=UserContactListResource, app=current_app)
    api_spec.spec.path(view=UserContactResource, app=current_app)


    # Me
    api_spec.spec.path(view=UserMeResource, app=current_app)
    api_spec.spec.path(view=UserMeAffairsResource, app=current_app)
