from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List

from domain.core.entity import Entity
from domain.users.entities.contact import ContactEntity
from domain.users.entities.group import UserPositionEntity


@dataclass_json
@dataclass
class UserEntity(Entity):
    """

    """
    first_name: str
    last_name: str
    contacts: List[ContactEntity] = field(default_factory=lambda: [])
    position: UserPositionEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
