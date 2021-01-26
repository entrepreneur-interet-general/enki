from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from domain.core.entity import Entity


@dataclass_json
@dataclass
class UserEntity(Entity):
    """

    """
    username: str
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
