from typing import Any, Dict, List
from uuid import uuid4

from flask import current_app
from marshmallow import ValidationError

from adapters.http.keycloak import KeycloakHelper
from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.affairs.schema.simple_affair import SimpleAffairSchema
from domain.affairs.services.affair_service import AffairService
from domain.users.entities.group import GroupType, UserPositionEntity, PositionGroupTypeEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.contact import ContactSchema
from domain.users.schemas.user import UserSchema
from entrypoints.config import EnkiConfig
from service_layer.unit_of_work import AbstractUnitOfWork


class UserService:
    schema = UserSchema

    @staticmethod
    def add_user(data: dict,
                 uow: AbstractUnitOfWork):
        try:
            user: UserEntity = UserService.schema().load(data)
        except ValidationError as ve:
            raise ve

        with uow:
            _ = uow.user.add(user)

            user_position = UserService.build_position_from_group_id_ad_position_id(
                group_id=user.group_id,
                position_id=user.position_id,
                group_type=user.group_type,
                uow=uow
            )
            user.position = user_position

            UserService.handle_keycloak(
                uuid=user.uuid,
                first_name=user.first_name,
                last_name=user.last_name,
                group_type=user.group_type,
                fonction=user.position.position.slug
            )

            uuid = str(user.uuid)

        return UserService.get_by_uuid(uuid=uuid, uow=uow)

    @staticmethod
    def handle_keycloak(uuid: str, first_name: str, last_name: str,
                        fonction: str, group_type: str):
        kh = KeycloakHelper.from_config(EnkiConfig())

        kh.update_user_at_creation(
            user_id=uuid,
            first_name=first_name,
            last_name=last_name,
            attributes={
                "fonction": fonction,
                "group_type": group_type,
            }
        )
        kh.assign_to_group(user_id=uuid, group_name=fonction.lower())

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
    def search_users(query: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            users: List[UserEntity] = uow.user.search(query=query)
            return UserService.schema(many=True).dump(users)

    @staticmethod
    def list_contacts(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            contacts: List[UserEntity] = uow.user.get_user_contacts(uuid=uuid)
            return ContactSchema(many=True).dump(contacts)

    @staticmethod
    def get_user_contact(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.get_user_contact(uuid=uuid, contact=contact)
            return ContactSchema(many=True).dump(contact)

    @staticmethod
    def add_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.add_user_contact(uuid=uuid, contact=contact)
            return ContactSchema().dump(contact)

    @staticmethod
    def remove_contact_to_user(uuid: str, contact_uuid: str, uow: AbstractUnitOfWork):
        with uow:
            contact = uow.contact.get_by_uuid(uuid=contact_uuid)
            uow.user.remove_user_contact(uuid=uuid, contact=contact)
            return ContactSchema().dump(contact)

    @staticmethod
    def get_affairs_by_user_uuid(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=uuid)
            affairs: List[SimpleAffairEntity] = uow.simple_affair.match_polygons(
                polygon=user.position.group.location.polygon
            )
            return SimpleAffairSchema(many=True).dump(affairs)

    @staticmethod
    def build_position_from_group_id_ad_position_id(
            group_id: str, position_id: str, group_type: str, uow: AbstractUnitOfWork
    ):
        group = uow.group.get_by_uuid(uuid=group_id)
        current_app.logger.info(f"GRoup {group.type} => {group_type}")
        if group.type != group_type:
            raise IndexError

        position: PositionGroupTypeEntity = uow.group.get_position(position_id=position_id)
        current_app.logger.info(f"Position {position.group_type} => {group_type}")
        if position.group_type != group_type:
            raise IndexError

        user_position = UserPositionEntity(uuid=str(uuid4()))
        user_position.group = group
        user_position.position = position
        uow.group.add_position(user_position)
        return user_position
