from typing import List, Union

from sqlalchemy.orm import Session

from domain.users.ports.group_repository import AbstractGroupRepository, AlreadyExistingGroupUuid
from domain.users.entities.group import GroupEntity
from .repository import PgRepositoryMixin

tagsList = List[GroupEntity]


class PgGroupRepository(PgRepositoryMixin, AbstractGroupRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=GroupEntity)
        AbstractGroupRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[GroupEntity, None]:
        matches = self.session.query(GroupEntity).filter(GroupEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def get_all(self) -> tagsList:
        return self.session.query(self.entity_type).all()
