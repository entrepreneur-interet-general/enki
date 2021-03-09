from datetime import datetime
from typing import Any, Dict, List

from flask import current_app
from marshmallow import ValidationError

from domain.affairs.entities.simple_affair_entity import SimpleAffairEntity
from domain.evenements.entities.evenement_entity import EvenementEntity
from domain.evenements.schemas.evenement_schema import EvenementSchema
from domain.evenements.entities.message_entity import MessageEntity
from domain.users.entities.user import UserEntity
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
            final_evenement: UserEntity = uow.evenement.get_by_uuid(uuid=evenement.uuid)
            return EvenementService.schema().dump(final_evenement)

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

    def finish_evenement(uuid: str, uow: AbstractUnitOfWork):
        with uow:
            evenement: EvenementEntity = uow.evenement.get_by_uuid(uuid=uuid)
            evenement.ended_at = datetime.now()
            return EvenementService.schema().dump(evenement)


