from adapters.http.keycloak import KeycloakHelper
from domain.users.entities.invitation import InvitationEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.invitation import InvitationSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class InvitationService:
    schema = InvitationSchema

    @staticmethod
    def create_invitation(data: dict,
                          uow: AbstractUnitOfWork):
        kh = KeycloakHelper.from_config(EnkiConfig())
        with uow:
            invitation: InvitationEntity = InvitationService.schema().load(data)
            user: UserEntity = uow.user.get_by_uuid(uuid=invitation.creator_id)
            uow.invitation.add(invitation)
            invitation.creator = user
            if invitation.email:
                user_id: str = InvitationService.create_user_from_email(kh=kh, email=invitation.email)
                InvitationService.send_reset_email(kh=kh, user_id=user_id)
            else:
                return InvitationSchema().dump(invitation)

    @staticmethod
    def token_with_email(token: str, email: str, uow: AbstractUnitOfWork):
        kh = KeycloakHelper.from_config(EnkiConfig())
        with uow:
            invitation: InvitationEntity = uow.invitation.get_by_token(token=token)
            user_id: str = InvitationService.create_user_from_email(kh=kh, email=email)
            invitation.validate(email=email, user_id=user_id)
            InvitationService.send_reset_email(kh=kh, user_id=user_id)
            return True

    @staticmethod
    def create_user_from_email(kh: KeycloakHelper, email: str) -> str:
        user_id = kh.create_user_from_invitation(email=email)
        return user_id

    @staticmethod
    def send_reset_email(kh: KeycloakHelper, user_id: str):
        kh.send_update_email(user_id=user_id)
