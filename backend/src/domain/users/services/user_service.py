from typing import Any, Dict, List
from marshmallow import ValidationError

from adapters.http.keycloak import KeycloakHelper
from domain.affairs.services.affair_service import AffairService
from domain.users.entities.group import UserPositionEntity, GroupType
from domain.users.entities.user import UserEntity
from domain.users.schemas.user import UserSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class UserService:
    schema = UserSchema

    @staticmethod
    def add_user(data: dict,
                 uow: AbstractUnitOfWork):

        code_insee = data.pop("code_insee", None)
        code_dept = data.pop("code_dept", None)
        try:
            user: UserEntity = UserService.schema().load(data)
            return_value = UserService.schema().dump(user)
        except ValidationError as ve:
            raise ve

        with uow:
            kh = KeycloakHelper.from_config(EnkiConfig())
            _ = uow.user.add(user)
            kh.update_user_at_creation(
                user_id=user.uuid,
                first_name=user.first_name,
                last_name=user.last_name,
                attributes={
                    "fonction": user.position,
                    "code_insee": code_insee,
                    "code_dept": code_dept,
                }
            )
            kh.assign_to_group(user_id=user.uuid, group_name=str(user.position).lower())

        return return_value

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return UserService.schema().dump(uow.user.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_users(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.get_all()
            return UserService.schema(many=True).dump(users)

    @staticmethod
    def list_contacts(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.get_user_contacts(uuid=uuid)
            return UserService.schema(many=True).dump(users)

    @staticmethod
    def get_user_contact(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.get_user_contact(uuid=uuid, contact=contact)

    @staticmethod
    def add_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.add_user_contact(uuid=uuid, contact=contact)

    @staticmethod
    def remove_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.remove_user_contact(uuid=uuid, contact=contact)

    @staticmethod
    def get_affairs_by_user_uuid(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
        code: str = user.position.group.location.external_id
        group_type: GroupType = user.position.group.type
        args = {
            "insee_code": code
        } if group_type.MAIRIE else {
            "dept_code": code
        }
        return AffairService.list_affairs_by_insee_and_postal_codes(**args)
