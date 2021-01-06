from .affair_ressource import AffairListResource, AffairResource
from .random_affair_resource import  AffairRandomResource, AffairRandomListResource
from .task_ressource import TaskResource, TaskListResource, TaskTagResource, TaskTagListResource
from .tag_ressources import TagResource, TagListResource
from .evenement_resource import EvenementListResource, EvenementResource
from .information_ressource import InformationResource, InformationListResource, InformationTagListResource, InformationTagResource
__all__ = [
    TaskResource, TaskListResource, TaskTagResource,TaskTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairResource,
    AffairRandomResource, AffairRandomListResource,
    EvenementListResource, EvenementResource,
    InformationResource, InformationListResource, InformationTagListResource, InformationTagResource
]