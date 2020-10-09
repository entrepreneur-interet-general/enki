from dataclasses import dataclass, field
from datetime import datetime
from dataclasses_json import dataclass_json
from domain.entities.base_entity import BaseEntity


@dataclass_json
@dataclass
class TagEntity(BaseEntity):
    title: str = field(default_factory=lambda: datetime.now())
    description: str = field(default_factory=lambda: datetime.now())
    creator_id: str = field(default_factory=lambda: datetime.now())
    color: str = field(default_factory=lambda: datetime.now())

    def __eq__(self, other):
        return self.uuid == other.uuid
