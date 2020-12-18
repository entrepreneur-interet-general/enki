from datetime import datetime
from typing import Any, Dict, List, Union

from marshmallow import ValidationError

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository
from domain.evenements.schema import EvenementSchema
from service_layer.unit_of_work import AbstractUnitOfWork


class EvenementService:
    schema = EvenementSchema()

    @staticmethod
    def add_evenement(data: dict,
                      uow: AbstractUnitOfWork):
        try:
            evenement: EvenementEntity = EvenementSchema().load(data)
        except ValidationError as ve:
            raise ve
        with uow:
            uow.evenement.add(evenement)

    @staticmethod
    def get_by_uuid(uuid: str, uow: AbstractUnitOfWork) -> Dict[str, Any]:
        with uow:
            return EvenementService.schema.dump(uow.evenement.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_evenements(uow: AbstractUnitOfWork) -> List[Dict[str, Any]]:
        with uow:
            evenements: List[EvenementEntity] = uow.evenement.get_all()
            serialized_evenements = [EvenementService.schema.dump(evenement) for evenement in evenements]
            return serialized_evenements
