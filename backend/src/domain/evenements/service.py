from datetime import datetime
from typing import Any, Dict, List, Union

from marshmallow import ValidationError

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository
from domain.evenements.schema import EvenementSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class EvenementService:
    schema = EvenementSchema

    @staticmethod
    def add_evenement(data: dict,
                      uow: AbstractUnitOfWork):
        try:
            evenement: EvenementEntity = EvenementService.schema().load(data)
            return_value = EvenementService.schema().dump(evenement)
        except ValidationError as ve:
            raise ve

        with uow:
            _ = uow.evenement.add(evenement)
        return return_value

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return EvenementService.schema().dump(uow.evenement.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_evenements(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.get_all()
            return EvenementService.schema(many=True).dump(evenements)
