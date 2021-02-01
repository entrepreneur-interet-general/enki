from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import Optional, List

from domain.core.entity import Entity


@dataclass_json
@dataclass
class UserEntity(Entity):
    """

    """
    first_name: str
    last_name: str
    position: str
    groups: List = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
