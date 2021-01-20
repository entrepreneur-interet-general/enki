from dataclasses import dataclass
from dataclasses_json import dataclass_json

from domain.core.entity import Entity


@dataclass_json
@dataclass
class GroupEntity(Entity):
    name: str
    description: str
