from typing import List, Union

from sqlalchemy.orm import Session

from domain.users.entities.invitation import InvitationEntity
from domain.users.ports.invitation_repository import AbstractInvitationRepository, AlreadyExistingInvitationUuid
from .repository import PgRepositoryMixin

invitationsList = List[InvitationEntity]


class PgInvitationRepository(PgRepositoryMixin, AbstractInvitationRepository):
    def __init__(self, session: Session):
        PgRepositoryMixin.__init__(self, session=session, entity_type=InvitationEntity)
        AbstractInvitationRepository.__init__(self)

    def _match_uuid(self, uuid: str) -> Union[InvitationEntity, None]:
        matches = self.session.query(InvitationEntity).filter(InvitationEntity.uuid == uuid).all()
        if not matches:
            return None
        return matches[0]

    def _match_token(self, token: str) -> Union[InvitationEntity, None]:
        matches = self.session.query(InvitationEntity).filter(InvitationEntity.token == token).all()
        if not matches:
            return None
        return matches[0]

    def _add(self, invitation: InvitationEntity):
        if self._match_uuid(invitation.uuid):
            raise AlreadyExistingInvitationUuid()
        self.session.add(invitation)

    def get_all(self) -> invitationsList:
        return self.session.query(self.entity_type).all()
