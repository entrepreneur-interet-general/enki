from .affair_ressource import AffairListResource, AffairResource
from .random_affair_resource import  AffairRandomResource, AffairRandomListResource
from .message_ressource import MessageResource, MessageListResource, MessageTagResource, MessageTagListResource
from .tag_ressources import TagResource, TagListResource
from .evenement_resource import EvenementListResource, EvenementResource
__all__ = [
    MessageResource, MessageListResource, MessageTagResource,MessageTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairResource,
    AffairRandomResource, AffairRandomListResource,
    EvenementListResource, EvenementResource,
]