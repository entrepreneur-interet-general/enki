from .affair_ressource import AffairListResource, AffairRandomResource, AffairRandomListResource
from .task_ressource import TaskResource, TaskListResource, TaskTagResource, TaskTagListResource
from .tag_ressources import TagResource, TagListResource

__all__ = [
    TaskResource, TaskListResource, TaskTagResource,TaskTagListResource,
    TagResource, TagListResource,
    AffairListResource, AffairRandomResource, AffairRandomListResource
]