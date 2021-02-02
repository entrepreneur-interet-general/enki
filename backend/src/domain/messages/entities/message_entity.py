from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum

from typing import Union, List

from domain.core.entity import Entity


class Severity(Enum):
    EXTREME = 1
    SEVERE = 2
    MODERATE = 3
    MINOR = 4
    UNKNOWN = 5


class MessageType(str, Enum):
    INFORMATION = "info"
    ASK = "ask"
    DO = "do"
    NEED_INFO = "need_info"
    UNKNOWN = "unknown"


@dataclass_json
@dataclass
class MessageEntity(Entity):
    title: str
    description: str
    evenement_id: str
    severity: Severity = field(default_factory=lambda: Severity.UNKNOWN)
    creator_id: Union[str, None] = field(default_factory=lambda: None)
    creator_name: Union[str, None] = field(default_factory=lambda: None)
    started_at: Union[datetime, None] = field(default_factory=lambda: None)
    tags: List = field(default_factory=lambda: [])
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())
    type: MessageType = field(default_factory=lambda: MessageType.UNKNOWN)
    executor_id: Union[str, None] = field(default_factory=lambda: None)
    done_at: Union[datetime, None] = field(default_factory=lambda: None)

    def __eq__(self, other):
        return self.uuid == other.uuid
