from typing import Optional, Union
from domain.core.entity import Entity
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TagEntity(Entity):
    title: str
    creator_id: Union[str, None] = field(default_factory=lambda: None)