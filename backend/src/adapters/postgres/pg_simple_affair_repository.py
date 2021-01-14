from typing import List, Union

from sqlalchemy.orm import Session

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.ports.affair_repository import AbstractAffairRepository, AlreadyExistingAffairUuid
from domain.affairs.ports.simple_affair_repository import AbstractSimpleAffairRepository
from domain.evenements.entity import EvenementEntity
from .repository import PgRepositoryMixin


class PgSimpleAffairRepository(PgRepositoryMixin, AbstractSimpleAffairRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=SimpleAffairEntity)
        AbstractAffairRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> SimpleAffairEntity:
        matches = self.session.query(SimpleAffairEntity).filter(SimpleAffairEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, affair: SimpleAffairEntity) -> None:
        if self._match_uuid(affair.uuid):
            raise AlreadyExistingAffairUuid()
        self.session.add(affair)
        self.commit()

    def get_all(self) -> List[SimpleAffairEntity]:
        return self.session.query(SimpleAffairEntity).all()

    def assign_evenement_to_affair(self, affair: SimpleAffairEntity, evenement: EvenementEntity) -> SimpleAffairEntity:
        affair.evenement_id = evenement.uuid
        self.commit()
        return affair

    def delete_affair_from_evenement(self, affair: SimpleAffairEntity) -> SimpleAffairEntity:
        affair.evenement_id = None
        self.commit()
        return affair

    def get_by_evenement(self, uuid: str) -> List[SimpleAffairEntity]:
        matches = self.session.query(SimpleAffairEntity).filter(SimpleAffairEntity.evenement_id == uuid).all()
        return matches