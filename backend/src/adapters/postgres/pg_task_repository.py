from typing import List

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin


class PgTaskRepository(AbstractTaskRepository, PgRepositoryMixin):

    def __init__(self, session: Session, tag_repo: AbstractTagRepository):
        super(AbstractTaskRepository, self).__init__(tag_repo=tag_repo)
        super(PgRepositoryMixin, self).__init__(session=session, entity_type=TaskEntity)

    def _add_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        p = self.session.query(TaskEntity).get(task.uuid)
        if p:
            t = self.session.query(TagEntity).get(tag_uuid)
            p.tags.append(t)
            self.commit()

    def _remove_tag_to_task(self, task: TaskEntity, tag_uuid: str) -> None:
        p = self.session.query(TaskEntity).get(task.uuid)
        if p:
            t = self.session.query(TagEntity).get(tag_uuid)
            p.tags.remove(t)
            self.commit()
