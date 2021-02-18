from datetime import datetime
from typing import Any, Dict, List, Union

from flask import current_app
from marshmallow import ValidationError

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository
from domain.evenements.schema import EvenementSchema
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
