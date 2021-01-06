from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List

from domain.core.entity import Entity
from domain.core.timestamped import TimeStamped


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


@dataclass_json
@dataclass
class MessageEventEntity(Entity, TimeStamped):
    title: str
    description: str
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    creator_id: Union[str, None] = field(default_factory=lambda: None)
    started_at: Union[datetime, None] = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])
