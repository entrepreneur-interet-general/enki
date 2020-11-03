from .affair_ressource import AffairListResource, AffairResource
from .random_affair_resource import  AffairRandomResource, AffairRandomListResource
from .task_ressource import TaskResource, TaskListResource, TaskTagResource, TaskTagListResource
from .tag_ressources import TagResource, TagListResource

__all__ = [
    TaskResource, TaskListResource, TaskTagResource,TaskTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairResource,
    AffairRandomResource, AffairRandomListResource
]