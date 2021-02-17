from typing import List, Union

from sqlalchemy.orm import Session

from domain.evenements.entity import EvenementEntity
from domain.evenements.repository import AbstractEvenementRepository, AlreadyExistingEvenementUuid
from .repository import PgRepositoryMixin


class PgEvenementRepository(PgRepositoryMixin, AbstractEvenementRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=EvenementEntity)

    def _match_uuid(self, uuid: str) -> Union[EvenementEntity, None]:
        matches = self.session.query(EvenementEntity).filter(EvenementEntity.uuid == uuid).all()
        if matches:
            return matches[0]

    def _add(self, evenement: EvenementEntity) -> None:
        if self._match_uuid(evenement.uuid):
            raise AlreadyExistingEvenementUuid()
        self.session.add(evenement)

    def get_all(self) -> List[EvenementEntity]:
        return self.session.query(self.entity_type).all()