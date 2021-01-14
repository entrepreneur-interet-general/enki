from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dataclasses_json import dataclass_json

from domain.core.entity import Entity


@dataclass_json
@dataclass
class SimpleAffairEntity(Entity):
    sge_hub_id: str
    evenement_id: Optional[str]
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
