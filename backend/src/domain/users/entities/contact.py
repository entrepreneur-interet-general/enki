from datetime import datetime
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict

from domain.core.entity import Entity
from dataclasses_json import DataClassJsonMixin


@dataclass
class ContactEntity(DataClassJsonMixin, Entity):
    first_name: str
    last_name: str
    position: str
    group_name: str
    creator_id: str
    email: str
    address: str
    tel: Dict[str, str]
    group_id: List = field(default_factory=lambda: [])
    group: List = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = field(default_factory=lambda: datetime.utcnow())
