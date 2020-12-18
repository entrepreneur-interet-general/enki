from typing import List, Union

from sqlalchemy.orm import Session

from domain.affairs.entities.affair_entity import AffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, affairsList
from domain.tasks.ports.task_repository import AlreadyExistingTaskUuid
from domain.tasks.entities.task_entity import TaskEntity
from .repository import PgRepositoryMixin


class PgAffairRepository(PgRepositoryMixin, AbstractAffairRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=AffairEntity)
        AbstractAffairRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> AffairEntity:
        matches = self.session.query(TaskEntity).filter(AffairEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, affair: AffairEntity) -> None:
        if self._match_uuid(affair.uuid):
            raise AlreadyExistingTaskUuid()
        self.session.add(affair)
        self.commit()

    def get_all(self) -> List[AffairEntity]:
        return self.session.query(AffairEntity).all()

    def _get_from_polygon(self, multipolygon: List) -> affairsList:
        return self.get_all()  # TODO: define postgres polygon query




