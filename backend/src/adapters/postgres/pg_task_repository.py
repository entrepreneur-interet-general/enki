from typing import List, Union

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, AlreadyExistingTaskUuid, NotFoundTask
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin


class PgTaskRepository(PgRepositoryMixin, AbstractTaskRepository):



    def __init__(self, session: Session, tag_repo: AbstractTagRepository):
        PgRepositoryMixin.__init__(self, session=session, entity_type=TaskEntity)
        AbstractTaskRepository.__init__(self, tag_repo=tag_repo)

    def _add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        p = self.session.query(TaskEntity).get(task.uuid)
        if p:
            t = self.session.query(TagEntity).get(tag.uuid)
            p.tags.append(t)
            self.commit()

    def _remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        p = self.session.query(TaskEntity).get(task.uuid)
        if p:
            t = self.session.query(TagEntity).get(tag.uuid)
            p.tags.remove(t)
            self.commit()

    def _match_uuid(self, uuid: str) -> TaskEntity:
        matches = self.session.query(TaskEntity).filter(TaskEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, task: TaskEntity) -> None:
        if self._match_uuid(task.uuid):
            raise AlreadyExistingTaskUuid()
        self.session.add(task)
        self.commit()

    def get_all(self) -> List[TaskEntity]:
        return self.session.query(self.entity_type).all()

    def _get_tag_by_task(self, uuid: str, tag_uuid: str) -> Union[TagEntity, None]:
        matches = self.session.query(TagEntity).\
            filter(TaskEntity.uuid == uuid).\
            filter(TagEntity.uuid == tag_uuid).all()
        if not matches:
            return None
        return matches[0]
