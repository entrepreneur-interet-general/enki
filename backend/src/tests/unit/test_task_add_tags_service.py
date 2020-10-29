from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.services.tag_service import TagService
from domain.tasks.services.task_service import TaskService
from uuid import uuid4


def test_add_task_and_add_tag(task_repo: AbstractTaskRepository):
    task_uuid = str(uuid4())
    tag_uuid = str(uuid4())
    TaskService.add_task(task_uuid, "Some title", "Some description", repo=task_repo)
    TagService.add_tag(tag_uuid, "Some title", repo=task_repo.tag_repo)

    TaskService.add_tag_to_task(task_uuid=task_uuid,
                                tag_uuid=tag_uuid,
                                repo=task_repo)

    task:TaskEntity = task_repo.get_by_uuid(task_uuid)
    tag:TagEntity = task_repo.tag_repo.get_by_uuid(tag_uuid)

    assert task.tags[0] == tag

def test_add_task_and_failed_to_add_tag_if_already_exists(task_repo: AbstractTaskRepository):
    pass
