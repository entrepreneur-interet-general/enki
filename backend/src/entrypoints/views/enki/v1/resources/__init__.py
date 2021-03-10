from .affair_evenement_ressource import AffairEvenementResource, AffairListEvenementResource
from .affair_ressource import AffairListResource, AffairResource
from .evenement_resource import EvenementListResource, EvenementResource, EvenementClosedResource
from .message_resource_resource import MessageResourceListResource, MessageResourceResource
from .message_ressource import MessageResource, MessageListResource
from .message_tag_resource import MessageTagResource, MessageTagListResource
from .random_affair_resource import AffairRandomResource, AffairRandomListResource
from .resource_ressources import ResourceListResource, ResourceResource
from .tag_ressources import TagResource, TagListResource

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
