from .affair_ressource import AffairListResource, AffairResource
from .random_affair_resource import AffairRandomResource, AffairRandomListResource
from .message_ressource import MessageResource, MessageListResource
from .message_tag_resource import MessageTagResource, MessageTagListResource
from .message_resource_resource import MessageResourceListResource, MessageResourceResource
from .tag_ressources import TagResource, TagListResource
from .evenement_resource import EvenementListResource, EvenementResource
from .resource_ressources import ResourceListResource, ResourceResource
from .resource_content_ressources import ResourceContentResource

__all__ = [
    MessageResource, MessageListResource,
    MessageTagResource, MessageTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairResource,
    AffairRandomResource, AffairRandomListResource,
    EvenementListResource, EvenementResource,
    ResourceListResource, ResourceResource,
    ResourceContentResource,
    MessageResourceListResource, MessageResourceResource
]
