from typing import Dict, Any

from adapters.http.keycloak import KeycloakHelper
from domain.users.entities.group import GroupEntity
from domain.users.entities.invitation import InvitationEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.group import GroupSchema
from domain.users.schemas.invitation import InvitationSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class InvitationService:
    schema = InvitationSchema

    @staticmethod
    def create_invitation(data: dict,
                          uow: AbstractUnitOfWork):
        with uow:
            invitation: InvitationEntity = InvitationService.schema().load(data)
            group = uow.group.get_by_uuid(uuid=invitation.group_id)
            if group.type != invitation.group_type:
                raise IndexError

            uow.invitation.add(invitation=invitation)

            return InvitationSchema().dump(invitation)

    @staticmethod
    def get_invitation_info(token: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            invitation: InvitationEntity = uow.invitation.get_by_token(token=token)
            invitation.validate()
            group: GroupEntity = uow.group.get_by_uuid(invitation.group_id)
            return {
                "group": GroupSchema().dump(group)
            }
