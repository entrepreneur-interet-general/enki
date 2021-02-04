from typing import List, Union

from sqlalchemy.orm import Session

from domain.users.ports.group_repository import AbstractGroupRepository, AlreadyExistingGroupUuid, GroupsList
from domain.users.entities.group import GroupEntity, GroupType, PositionGroupTypeEntity, LocationEntity
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

    def get_position_by_group_type(self, group_type: GroupType) -> List[PositionGroupTypeEntity]:
        matches: List[PositionGroupTypeEntity] = self.session.query(PositionGroupTypeEntity).filter(
            PositionGroupTypeEntity.group_type == group_type).all()
        return matches

    def get_location_by_query(self, query: str) -> List[LocationEntity]:
        matches = self.session.query(LocationEntity).filter(
            LocationEntity.search_label.match(query)).all()
        return matches
