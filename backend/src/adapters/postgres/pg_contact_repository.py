from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session

from domain.users.entities.group import UserPositionEntity, PositionGroupTypeEntity, GroupEntity
from domain.users.ports.contact_repository import AbstractContactRepository, AlreadyExistingContactUuid
from domain.users.entities.contact import ContactEntity
from .repository import PgRepositoryMixin

contactsList = List[ContactEntity]


class PgContactRepository(PgRepositoryMixin, AbstractContactRepository):

    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=ContactEntity)
        AbstractContactRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[ContactEntity, None]:
        matches = self.session.query(ContactEntity).filter(ContactEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> contactsList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def _add(self, contact: ContactEntity):
        if self._match_uuid(contact.uuid):
            raise AlreadyExistingContactUuid()
        self.session.add(contact)

    def get_all(self) -> contactsList:
        return self.session.query(self.entity_type).all()

    def get_by_query(self, query):
        matches = self.session.query(self.entity_type).\
            join(UserPositionEntity).\
            join(PositionGroupTypeEntity).\
            join(GroupEntity).\
            filter(
            or_(
                self.entity_type.full_name.match(query),
                PositionGroupTypeEntity.label.match(query),
                GroupEntity.label.match(query),
            )
        ).all()
        return matches

