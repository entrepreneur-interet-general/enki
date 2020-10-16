from typing import List

from sqlalchemy.orm import Session

from domain.tasks.ports.task_repository import AbstractTaskRepository
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin, NotFoundException



class PgTaskRepository(AbstractTaskRepository):

    def __init__(self, session: Session):
        super().__init__(session=session, entity_type=TagEntity)
        self.session = session

    def get_all(self) -> List[TaskEntity]:
        return self.session.query(TaskEntity).all()

    def _add(self, task: TaskEntity):
        self.session.add(task)
        self.commit()

    def _match_uuid(self, uuid: str):
        matches = self.session.query(TaskEntity).filter(TaskEntity.uuid == uuid).all()
        if not matches:
            raise NotFoundException
        return matches[0]

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

    def commit(self):
        self.session.commit()

