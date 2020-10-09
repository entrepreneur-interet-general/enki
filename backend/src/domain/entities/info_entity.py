from dataclasses import dataclass, field
from datetime import datetime

from .event_entity import EventEntity


@dataclass
class InformationEntity(EventEntity):
    event_type: str = field(default="information")
    executor_id: str = field(default_factory=lambda: None)
    executor_type: str = field(default_factory=lambda: None)
    user_ids: str = field(default_factory=list)
