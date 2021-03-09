from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Optional

from domain.core.entity import Entity
from dataclasses_json import DataClassJsonMixin

from domain.users.entities.group import UserPositionEntity


@dataclass
class ContactEntity(DataClassJsonMixin, Entity):
    first_name: str
    last_name: str
    email: str
    address: str
    tel: Dict[str, str]
    position_id: str
    group_id: str
    group_type: str
    position: UserPositionEntity = field(default_factory=lambda: None)
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
