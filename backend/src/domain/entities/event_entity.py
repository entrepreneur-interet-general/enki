from dataclasses import dataclass, field
from datetime import datetime
from .base_entity import BaseEntity
from enum import Enum


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


@dataclass
class EventEntity(BaseEntity):
    title: str = field(default_factory=lambda: None)
    description: str = field(default_factory=lambda: None)
    event_type: str = field(default_factory=lambda: None)
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    creator_id: str = field(default_factory=lambda: None)
    creator_type: str = field(default_factory=lambda: None)
    started_at: datetime = field(default_factory=lambda: None)
    #parents: any = field(default_factory=lambda: None)
    #childs: any = field(default_factory=lambda: None)
