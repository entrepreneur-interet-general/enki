import abc
from typing import List, Union

from werkzeug.exceptions import HTTPException

from domain.users.entities.invitation import InvitationEntity

InvitationsList = List[InvitationEntity]


class AlreadyExistingInvitationUuid(HTTPException):
    code = 409
    description = "Invitation already exists"


class NotFoundInvitation(HTTPException):
    code = 404
    description = "Invitation not found"


class AbstractInvitationRepository(abc.ABC):
    def add(self, invitation: InvitationEntity) -> None:
        if self._match_uuid(invitation.uuid):
            raise AlreadyExistingInvitationUuid()
        self._add(invitation)

    def get_by_uuid(self, uuid: str) -> InvitationEntity:
        matches = self._match_uuid(uuid)
        if not matches:
            raise NotFoundInvitation
        return matches

    def get_by_token(self, token: str) -> InvitationEntity:
        matches = self._match_token(token)
        if not matches:
            raise NotFoundInvitation
        return matches

    @abc.abstractmethod
    def _add(self, invitation: InvitationEntity) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_uuid(self, uuid: str) -> Union[InvitationEntity, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def _match_token(self, token: str) -> Union[InvitationEntity, None]:
        raise NotImplementedError
