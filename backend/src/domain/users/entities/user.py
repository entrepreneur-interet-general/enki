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
    position_id: str = field(default_factory=lambda: None)
    group_id: str = field(default_factory=lambda: None)
    group_type: str = field(default_factory=lambda: None)
    contacts: List[ContactEntity] = field(default_factory=lambda: [])
    position: UserPositionEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())

    def __repr__(self):
        return f"UserEntity {self.uuid} : {self.first_name}, {self.last_name}"
