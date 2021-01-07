from typing import List, Union

from sqlalchemy.orm import Session

from domain.tasks.ports.tag_repository import AbstractTagRepository
from domain.tasks.ports.task_repository import AbstractTaskRepository, AlreadyExistingTaskUuid, NotFoundTask, TasksList
from domain.tasks.entities.task_entity import TaskEntity
from domain.tasks.entities.tag_entity import TagEntity
from .repository import PgRepositoryMixin


class PgTaskRepository(PgRepositoryMixin, AbstractTaskRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=TaskEntity)
        AbstractTaskRepository.__init__(self)

    def add_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.append(tag)
        self.commit()

    def remove_tag_to_task(self, task: TaskEntity, tag: TagEntity) -> None:
        task.tags.remove(tag)
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
        match = self.get_by_uuid(uuid=uuid)
        matches = [tag for tag in match.tags if tag.uuid == tag_uuid]
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> TasksList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches


