from typing import List, Union

from sqlalchemy.orm import Session

from domain.users.entities.contact import ContactEntity
from domain.users.ports.user_repository import AbstractUserRepository, AlreadyExistingUserUuid
from domain.users.entities.user import UserEntity
from .repository import PgRepositoryMixin

usersList = List[UserEntity]


class PgUserRepository(PgRepositoryMixin, AbstractUserRepository):


    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=UserEntity)
        AbstractUserRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[UserEntity, None]:
        matches = self.session.query(UserEntity).filter(UserEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _match_uuids(self, uuids: List[str]) -> usersList:
        matches = self.session.query(self.entity_type).filter(self.entity_type.uuid.in_(uuids)).all()
        return matches

    def _add(self, user: UserEntity):
        if self._match_uuid(user.uuid):
            raise AlreadyExistingUserUuid()
        self.session.add(user)
        self.commit()

    def get_all(self) -> usersList:
        return self.session.query(self.entity_type).all()

    def _get_user_contacts(self, user: UserEntity):
        return user.contacts

    def _get_user_contact(self, user: UserEntity, contact: ContactEntity):
        matches = [contact for contact in user.contacts if contact.uuid == contact.uuid]
        if not matches:
            return None
        return matches[0]

    def _add_user_contact(self, user: UserEntity, contact: ContactEntity):
        user.contacts.append(contact)
        self.commit()

    def _remove_user_contact(self, user: UserEntity, contact: ContactEntity):
        user.contacts.remove(contact)
        self.commit()
