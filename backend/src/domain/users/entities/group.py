from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Dict

from domain.core.entity import Entity


class GroupType(str, Enum):
    MAIRIE = "mairie"
    PREFECTURE = "prefecture"
    PARTENAIRE = "partenaire"
    SDIS = "SDIS"
    COZ = "COZ"


@dataclass_json
@dataclass
class GroupEntity(Entity):
    name: str
    type: GroupType
    location: Dict[str, str]
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
