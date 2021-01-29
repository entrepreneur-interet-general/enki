from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from domain.core.entity import Entity


class CompanyType(str, Enum):
    MAIRIE = "mairie"
    PREFECTURE = "prefecture"
    PARTENAIRE = "partenaire"
    SDIS = "SDIS"
    COZ = "COZ"


@dataclass_json
@dataclass
class CompanyEntity(Entity):
    name: str
    type: CompanyType
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
