from datetime import datetime
from typing import Any, Dict, List, Union

from domain.evenements.entity import EvenementEntity, EvenementType
from domain.evenements.repository import AbstractEvenementRepository


class EvenementService:
    @staticmethod
    def add_evenement(uuid: str,
                      title: str,
                      description: str,
                      type: EvenementType,
                      started_at: datetime,
                      ended_at: Union[datetime, None],
                      creator_id: str,
                      repo: AbstractEvenementRepository):
        evenement: EvenementEntity = EvenementEntity(uuid=uuid,
                                                     title=title,
                                                     description=description,
                                                     type=type,
                                                     started_at=started_at,
                                                     ended_at=ended_at,
                                                     creator_id=creator_id, )
        repo.add(evenement)

    @staticmethod
    def get_by_uuid(uuid: str, repo: AbstractEvenementRepository):
        return repo.get_by_uuid(uuid=uuid).to_dict()

    @staticmethod
    def list_evenements(repo: AbstractEvenementRepository) -> List[Dict[str, Any]]:
        evenements: List[EvenementEntity] = repo.get_all()
        serialized_evenements = [evenement.to_dict() for evenement in evenements]
        return serialized_evenements
