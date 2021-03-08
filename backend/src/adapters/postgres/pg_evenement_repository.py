from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session, lazyload

from domain.evenements.entity import EvenementEntity, UserEvenementRole
from domain.evenements.repository import AbstractEvenementRepository
from .repository import PgRepositoryMixin


class PgEvenementRepository(PgRepositoryMixin, AbstractEvenementRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=EvenementEntity)

    def _match_uuid(self, uuid: str) -> Union[EvenementEntity, None]:
        matches = self.session.query(EvenementEntity).options(lazyload('*')).filter(EvenementEntity.uuid == uuid).all()
        if matches:
            return matches[0]

    def _add(self, evenement: EvenementEntity) -> None:
        self.session.add(evenement)

    def get_all(self) -> List[EvenementEntity]:
        return self.session.query(self.entity_type).options(lazyload('*')).all()

    def _add_user_role(self, user_role: UserEvenementRole):
        self.session.add(user_role)

    def _match_user_event(self, user_role: UserEvenementRole):
        matches = self.session.query(UserEvenementRole). \
            filter(UserEvenementRole.evenement_id == user_role.evenement_id). \
            filter(UserEvenementRole.user_id == user_role.user_id).all()
        if matches:
            return matches[0]

    def list_from_user_id(self, user_uuid: str) -> List[EvenementEntity]:
        return self.session.query(self.entity_type).join(UserEvenementRole).options(lazyload('*')).filter(
            or_(
                EvenementEntity.creator_id == user_uuid,
                UserEvenementRole.user_id == user_uuid
            )
        ).all()