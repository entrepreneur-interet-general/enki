import json

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from domain.affairs.entities.affair_entity import AffairEntity
from domain.core.entity import Entity
from domain.evenements.entity import EvenementEntity
from entrypoints.serializers import EnkiJsonEncoder


@dataclass_json
@dataclass
class SimpleAffairEntity(Entity):
    sge_hub_id: str
    default_affair: AffairEntity = None
    affair: dict = field(init=False)
    location: str = field(init=False)
    evenement_id: Optional[str] = None
    evenement: Optional[EvenementEntity] = None
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __post_init__(self):
        self.location = self.default_affair.geom_location
        self.affair = json.loads(EnkiJsonEncoder().encode(self.default_affair.to_dict()))
