from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum
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
    event_type: str
    severity: Severity
    creator_id: str
    creator_type: str
    started_at: datetime

    # parents: any = field(default_factory=lambda: None)
    # childs: any = field(default_factory=lambda: None)
