from entrypoints.views.enki.v1.resources.affairs.affair_evenement_ressource import AffairEvenementResource, AffairListEvenementResource
from entrypoints.views.enki.v1.resources.affairs.affair_ressource import AffairListResource, AffairResource
from entrypoints.views.enki.v1.resources.evenements.evenement_resource import EvenementListResource, EvenementResource, EvenementClosedResource
from entrypoints.views.enki.v1.resources.evenements.message_resource_resource import MessageResourceListResource, MessageResourceResource
from entrypoints.views.enki.v1.resources.evenements.message_ressource import MessageResource, MessageListResource
from entrypoints.views.enki.v1.resources.evenements.message_tag_resource import MessageTagResource, MessageTagListResource
from entrypoints.views.enki.v1.resources.affairs.random_affair_resource import AffairRandomResource, AffairRandomListResource
from entrypoints.views.enki.v1.resources.evenements.resource_ressources import ResourceListResource, ResourceResource
from entrypoints.views.enki.v1.resources.evenements.tag_ressources import TagResource, TagListResource

__all__ = [
    MessageResource, MessageListResource,
    MessageTagResource, MessageTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairResource,
    AffairRandomResource, AffairRandomListResource,
    EvenementListResource, EvenementResource, EvenementClosedResource,
    ResourceListResource, ResourceResource,
    MessageResourceListResource, MessageResourceResource,
    AffairEvenementResource, AffairListEvenementResource,
]
