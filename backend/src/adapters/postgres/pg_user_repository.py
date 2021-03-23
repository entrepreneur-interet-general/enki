from typing import List, Union, Optional

from flask import current_app
from sqlalchemy import or_
from sqlalchemy.orm import Session, lazyload

from domain.users.entities.group import UserPositionEntity, PositionGroupTypeEntity, GroupEntity
from domain.users.entities.user import UserEntity
from domain.users.ports.user_repository import AbstractUserRepository, AlreadyExistingUserUuid
from .repository import PgRepositoryMixin

usersList = List[UserEntity]


class PgUserRepository(PgRepositoryMixin, AbstractUserRepository):


    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=UserEntity)
        AbstractUserRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[UserEntity, None]:
        matches = self.session.query(UserEntity).options(lazyload('*')).filter(UserEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> usersList:
        matches = self.session.query(self.entity_type).options(lazyload('*')).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def _add(self, user: UserEntity):
        if self._match_uuid(user.uuid):
            raise AlreadyExistingUserUuid(uuid=user.uuid)
        self.session.add(user)

    def get_all(self) -> usersList:
        return self.session.query(self.entity_type).all()

    def search(self, query: str, uuids: Optional[List[str]] = None, limit=10) -> usersList:
        match_query = self.session.query(self.entity_type).\
            join(UserPositionEntity).\
            join(PositionGroupTypeEntity).\
            join(GroupEntity).\
            filter(
            or_(
                self.entity_type.full_name.match(query),
                PositionGroupTypeEntity.label.match(query),
                GroupEntity.label.match(query),
            )
        )
        if uuids:
            match_query = match_query.filter(self.entity_type.uuid.notin_(uuids))
        matches = match_query.limit(limit).all()
        return matches