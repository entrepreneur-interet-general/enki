from typing import Optional
from domain.core.entity import Entity
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class TagEntity(Entity):
    title: str
    description: Optional[str]
    creator_id: str
    color: str
