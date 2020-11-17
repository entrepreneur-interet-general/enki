from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List

from domain.core.entity import TimeStampedEntity
from domain.tasks.entities.resource_entity import ResourceEntity


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


@dataclass_json
@dataclass
class MessageEventEntity(TimeStampedEntity):
    title: str
    description: str
    event_type: str
    resources: List[ResourceEntity] = field(default_factory=lambda: [])
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    creator_id: Union[str, None] = field(default_factory=lambda: None)
    creator_type: Union[str, None] = field(default_factory=lambda: None)
    started_at: Union[datetime, None] = field(default_factory=lambda: None)

    # parents: any = field(default_factory=lambda: None)
    # childs: any = field(default_factory=lambda: None)
