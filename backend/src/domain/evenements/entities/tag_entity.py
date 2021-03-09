from dataclasses import dataclass, field
from datetime import datetime
from typing import Union

from dataclasses_json import dataclass_json

from domain.core.entity import Entity


@dataclass_json
@dataclass
class TagEntity(Entity):
    title: str
    creator_id: Union[str, None] = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
