from datetime import datetime
from typing import Any, Dict, List, Union

from marshmallow import ValidationError

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository
from domain.evenements.schema import EvenementSchema


class EvenementService:
    @staticmethod
    def add_evenement(data: dict,
                      repo: AbstractEvenementRepository):
        try:
            evenement: EvenementEntity = EvenementSchema().load(data)
        except ValidationError as ve:
            raise

        repo.add(evenement)

    @staticmethod
    def get_by_uuid(uuid: str, repo: AbstractEvenementRepository):
        return EvenementSchema().dump(repo.get_by_uuid(uuid=uuid))

    @staticmethod
    def list_evenements(repo: AbstractEvenementRepository) -> List[Dict[str, Any]]:
        schema = EvenementSchema()
        evenements: List[EvenementEntity] = repo.get_all()
        serialized_evenements = [schema.dump(evenement) for evenement in evenements]
        return serialized_evenements
