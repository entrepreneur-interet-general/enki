from datetime import datetime
from typing import Any, Dict, List, Union
from uuid import uuid4

from flask import current_app
from marshmallow import ValidationError

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entity import EvenementEntity, UserEvenementRole, EvenementRoleType
from domain.evenements.schema import EvenementSchema
from domain.messages.entities.message_entity import MessageEntity
from domain.users.entities.user import UserEntity
from domain.users.schemas.user import UserSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class EvenementService:
    schema = EvenementSchema

    @staticmethod
    def add_evenement(data: dict,
                      uow: AbstractUnitOfWork):
        creator_id = data.pop("creator_id")
        try:
            evenement: EvenementEntity = EvenementService.schema().load(data)
        except ValidationError as ve:
            raise ve

        with uow:
            user: UserEntity = uow.user.get_by_uuid(uuid=creator_id)
            _ = uow.evenement.add(evenement)
            evenement.creator = user
            final_evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=evenement.uuid)
            return EvenementService.schema().dump(final_evenement)

    @staticmethod
    def invite_user(uuid: str, user_id: str, role_type: EvenementRoleType, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            user_event_role: UserEvenementRole = UserEvenementRole(
                uuid=str(uuid4()),
                user_id=user.uuid,
                evenement_id=evenement.uuid,
                type=role_type
            )
            user_event_role.user = user
            evenement.add_user_role(user_role=user_event_role)

            return UserSchema().dump(user)

    @staticmethod
    def change_user_role(uuid: str , user_id: str, role_type:EvenementRoleType, uow: AbstractUnitOfWork)-> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            evenement.change_access_type(user_id=user_id, role_type=role_type)
            return UserSchema().dump(user)

    @staticmethod
    def revoke_access(uuid: str , user_id: str, uow: AbstractUnitOfWork)-> Dict[str, Any]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            user: UserEntity = uow.user.get_by_uuid(uuid=user_id)
            evenement.revoke_user_access(user_id=user_id)
            return UserSchema().dump(user)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            current_app.logger.info(uow.evenement.get_by_uuid(uuid=uuid))
            return EvenementService.schema().dump(uow.evenement.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_evenements(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.get_all()
            return EvenementService.schema(many=True).dump(evenements)

    @staticmethod
    def get_all_messages_and_affairs(evenement_id: str, uow: AbstractUnitOfWork):
        with uow:
            messages: List[MessageEntity] = uow.message.get_messages_by_query(evenement_id=evenement_id,
                                                                              tag_ids=[])
            return messages

    @staticmethod
    def list_affairs_by_evenement(evenement_id: str, uow: AbstractUnitOfWork) -> List[SimpleAffairEntity]:
        with uow:
            simple_affairs: List[SimpleAffairEntity] = uow.simple_affair.get_by_evenement(uuid=evenement_id)
            return simple_affairs

    @staticmethod
    def get_evenements_by_user_id(user_uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.list_from_user_id(user_uuid=user_uuid)
            return EvenementService.schema(many=True).dump(evenements)

    @staticmethod
    def finish_evenement(uuid: str, uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            evenement.ended_at = datetime.now()
            return EvenementService.schema().dump(evenement)
