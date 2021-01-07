from domain.tasks.entities.tag_entity import TagEntity
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.services.tag_service import TagService
from domain.tasks.services.task_service import TaskService
from uuid import uuid4


def test_add_task_and_add_tag(task_repo: AbstractTaskRepository, tag_repo: AbstractTagRepository):
    task_uuid = str(uuid4())
    tag_uuid = str(uuid4())
    event_uuid = str(uuid4())
    task = TaskEntity(task_uuid, title="Some title", description="Some description", evenement_id=event_uuid)
    tag = TagEntity(tag_uuid, "Some title")
    task_repo.add(task)
    tag_repo.add(tag)
    added_task = task_repo.get_by_uuid(task_uuid)
    added_tag = tag_repo.get_by_uuid(tag_uuid)
    print(added_tag)

    task_repo.add_tag_to_task(task=added_task,
                              tag=added_tag)

    task: TaskEntity = task_repo.get_by_uuid(task_uuid)
    tag: TagEntity = tag_repo.get_by_uuid(tag_uuid)

    assert task.tags[0] == tag


def test_add_task_and_failed_to_add_tag_if_already_exists(task_repo: AbstractTaskRepository):
    pass
